#!/usr/bin/python2
import vcf
import re
splitre = re.compile('[|/]')


vcf_reader = vcf.Reader(open('/tmp/555/family.vcf.gz', 'r'))

Sickle_cell = { 'FATHER':1, 'MOTHER':1, 'DAUGHTER1':1, 'DAUGHTER2':2, 'DAUGHTER3':0, 'SON1':1, 'SON2':2 } 
Sickle_cell_size = len(Sickle_cell)

for record in vcf_reader:
	m = int(0)
	for call in record.samples:
		gts = splitre.split(call.data[0])
		gtsum = int(gts[0]) + int(gts[1])
		if (Sickle_cell[call.sample] != gtsum): break
		m+=1
	if(m==Sickle_cell_size):print record
