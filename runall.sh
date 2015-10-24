#!/bin/bash

gcc family.c -ggdb -O4 -o family; 

#sickle = Sickle Cell Anemia
#ssd =  Severe Skeletal Dysplasia
#spp =  Spastic Paraplegia
#retina = Retinitis Pigmentosa

./family sickle /tmp/family.vcf | pigz -9 > sickle.vcf.gz;
./family ssd /tmp/family.vcf    | pigz -9 > ssd.vcf.gz;
./family spp /tmp/family.vcf    | pigz -9 > spp.vcf.gz;
./family retina /tmp/family.vcf | pigz -9 > retina.vcf.gz;
