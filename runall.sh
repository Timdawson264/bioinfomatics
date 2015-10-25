#!/bin/bash

gcc family.c -ggdb -O4 -o family; 

#sickle = Sickle Cell Anemia
#ssd =  Severe Skeletal Dysplasia
#spp =  Spastic Paraplegia
#retina = Retinitis Pigmentosa

InputFile=/tmp/family.vcf
#InputFile=vcf/family_exons.vcf

./family sickle $InputFile | pigz -9 > vcf/sickle.vcf.gz;
./family ssd    $InputFile | pigz -9 > vcf/ssd.vcf.gz;
./family spp    $InputFile | pigz -9 > vcf/spp.vcf.gz;
./family retina $InputFile | pigz -9 > vcf/retina.vcf.gz;

#cat exons.txt | cut -f3,5,6 | sed -e 's/chr//' | grep -Pv "^(X|Y|M|U)"  | sed -re 's/_[^\t ]*//g' > allranges.txt 

