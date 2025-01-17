#!/usr/bin/python2
import sys

#DEFINES
COMMON_INDEX_CHROMOSOME = 0
COMMON_INDEX_LOCATION = 1
VARIANT_INDEX_CHROMOSOME = 0
VARIANT_INDEX_LOCATION = 1


def check_common_function():

	if(len(sys.argv)) != 3:
		print("USAGE: python check_exons.py common_file variants_file")
		return

	# open files
	common_file = open(sys.argv[1]);
	variant_file = open(sys.argv[2]);

	line = ""
	while not line.startswith('#CHROM'):
		line = variant_file.readline()

	# skip title row
	print line[:-1]

	# read first variant
	current_variant_line = variant_file.readline()[:-1]
	current_variant_split = current_variant_line.split("\t")
	current_variant_chromosome = int(current_variant_split[VARIANT_INDEX_CHROMOSOME])
	current_variant_location = int(current_variant_split[VARIANT_INDEX_LOCATION])

	# For every variant, check if it lies in the current region we are checking.
	# We move through the files based on the following conditions:
	# Condition 1: If the exonic region lies on the NEXT chromosome, we can move to the next variant.
	# Condition 2: If the exonic region lies on the PREVIOUS chromosome, we move to the next exonic region.
	# Condition 3: If the exonic region is BEFORE this variant, we can safely move to the next exonic region.
	# Condition 4: If the exonic region is AFTER this variant, we can safely move to the next variant.

	for common_variant in common_file:
		if(common_variant[0] == '#') | (common_variant[0] == '/'):
			continue

		# Split into array
		common_variant_split = common_variant[:-1].split("\t")

		# get chromosome, start, and end for exonic region
		common_variant_chromosome = int(common_variant_split[COMMON_INDEX_CHROMOSOME])
		common_variant_location = int(common_variant_split[COMMON_INDEX_LOCATION])

		if current_variant_chromosome > common_variant_chromosome:
			#z = "Current Chrom > Common Chrom"
			#print z, current_variant_chromosome, common_variant_chromosome
			continue

		# until we reach the end of this chromosome in the family variant file
		while current_variant_chromosome <= common_variant_chromosome:

			if current_variant_chromosome < common_variant_chromosome:
				#z = "Current Chrom < Common Chrom"
				print current_variant_line
				#print z, current_variant_chromosome, common_variant_chromosome
				current_variant_line = variant_file.readline()[:-1]
				current_variant_split = current_variant_line.split("\t")
				if current_variant_split == ['']:
					# We reached end of variant file. Done.
					return	
				current_variant_chromosome = int(current_variant_split[VARIANT_INDEX_CHROMOSOME])
				current_variant_location = int(current_variant_split[VARIANT_INDEX_LOCATION])
				continue

			'''
			if(current_variant_location == common_variant_location):
				print current_variant_line
				# Read next variant from variant file
				current_variant_line = variant_file.readline()[:-1]
				current_variant_split = current_variant_line.split("\t")
				if current_variant_split == ['']:
					# We reached end of variant file. Done.
					return
				current_variant_chromosome = int(current_variant_split[VARIANT_INDEX_CHROMOSOME])
				current_variant_location = int(current_variant_split[VARIANT_INDEX_LOCATION])
				break
			'''

			if(current_variant_location < common_variant_location):
				# Variant is in chromosome, and in exonic region.
				print current_variant_line
				
				# UNCOMMENT THE BELOW LINE TO PRINT THE REGION IT WAS FOUND IN
				# print exonic_region

			elif(current_variant_location > common_variant_location):
				# current variant is forward of this exonic region. Read next exonic region.
				break

			# Read next variant from variant file
			current_variant_line = variant_file.readline()[:-1]
			current_variant_split = current_variant_line.split("\t")
			if current_variant_split == ['']:
				# We reached end of variant file. Done.
				return
			current_variant_chromosome = int(current_variant_split[VARIANT_INDEX_CHROMOSOME])
			current_variant_location = int(current_variant_split[VARIANT_INDEX_LOCATION])
	#print 'end'
if __name__ == "__main__":
	check_common_function()
