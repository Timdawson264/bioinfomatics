#!/bin/bash

gcc family.c -ggdb -O4 -o family; 

#sickle = Sickle Cell Anemia
#ssd =  Severe Skeletal Dysplasia
#spp =  Spastic Paraplegia
#retina = Retinitis Pigmentosa

./family sickle /tmp/family.vcf > sickle.vcf;
./family ssd /tmp/family.vcf > ssd.vcf;
./family spp /tmp/family.vcf > spp.vcf;
./family retina /tmp/family.vcf > retina.vcf;

