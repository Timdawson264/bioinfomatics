#!/bin/bash

gcc family.c -ggdb -O4 -o family; 

#sickle = Sickle Cell Anemia
#ssd =  Severe Skeletal Dysplasia
#spp =  Spastic Paraplegia
#retina = Retinitis Pigmentosa

echo "Finding vatiations based on inheratance and expression"
InputFile=vcf/family.vcf
./family sickle $InputFile | pigz -9 > vcf/sickle.vcf.gz;
./family ssd    $InputFile | pigz -9 > vcf/ssd.vcf.gz;
./family spp    $InputFile | pigz -9 > vcf/spp.vcf.gz;
./family retina $InputFile | pigz -9 > vcf/retina.vcf.gz;

echo "Extacting coding regions"
ExonFile=exons_allranges_sorted.txt
zcat vcf/sickle.vcf.gz | python2 check_exons.py $ExonFile /dev/stdin | pigz -9 > exonic_region_vcf/sickle.vcf.gz
zcat vcf/ssd.vcf.gz | python2 check_exons.py $ExonFile /dev/stdin    | pigz -9 > exonic_region_vcf/ssd.vcf.gz
zcat vcf/spp.vcf.gz | python2 check_exons.py $ExonFile /dev/stdin    | pigz -9 > exonic_region_vcf/spp.vcf.gz
zcat vcf/retina.vcf.gz | python2 check_exons.py $ExonFile /dev/stdin | pigz -9 > exonic_region_vcf/retina.vcf.gz

echo "Removing common variatations"
SortedCommon=vcf/ALL_merged_sorted.vcf
zcat exonic_region_vcf/sickle.vcf.gz  |  python2 ./common_var.py $SortedCommon /dev/stdin | pigz -9 > uncommon/sickle.vcf.gz
zcat exonic_region_vcf/ssd.vcf.gz     |  python2 ./common_var.py $SortedCommon /dev/stdin | pigz -9 > uncommon/ssd.vcf.gz
zcat exonic_region_vcf/spp.vcf.gz     |  python2 ./common_var.py $SortedCommon /dev/stdin | pigz -9 > uncommon/spp.vcf.gz
zcat exonic_region_vcf/retina.vcf.gz  |  python2 ./common_var.py $SortedCommon /dev/stdin | pigz -9 > uncommon/retina.vcf.gz

echo "Running gene filter"
#Dysplasia.txt  Retinitis.txt  Sickle.txt  Spastic.txt

zcat uncommon/sickle.vcf.gz |  python2 ./exons_finder.py exons.sqlite /dev/stdin "Associated Genes/Sickle.txt"    > final_vcf/sickle.vcf
zcat uncommon/ssd.vcf.gz |  python2 ./exons_finder.py exons.sqlite /dev/stdin "Associated Genes/Dysplasia.txt"    > final_vcf/ssd.vcf
zcat uncommon/spp.vcf.gz |  python2 ./exons_finder.py exons.sqlite /dev/stdin "Associated Genes/Spastic.txt"      > final_vcf/spp.vcf
zcat uncommon/retina.vcf.gz |  python2 ./exons_finder.py exons.sqlite /dev/stdin "Associated Genes/Retinitis.txt" > final_vcf/retina.vcf

#cat exons.txt | cut -f3,5,6 | sed -e 's/chr//' | grep -Pv "^(X|Y|M|U)"  | sed -re 's/_[^\t ]*//g' > allranges.txt 

