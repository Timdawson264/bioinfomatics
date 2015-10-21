#!/usr/bin/python2
import sys

#DEFINES
EXONIC_INDEX_CHROMOSOME = 0
EXONIC_INDEX_START = 1
EXONIC_INDEX_END = 2
VARIANT_INDEX_CHROMOSOME = 0
VARIANT_INDEX_LOCATION = 1


def check_exon_function():

	if(len(sys.argv)) != 3:
		print("USAGE: python check_exons.py exon_file variance_file")
		return

	# open files
	exonic_file = open(sys.argv[1]);
	variant_file = open(sys.argv[2]);


	# skip title row
	print variant_file.readline()

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

	for exonic_region in exonic_file:
		# Split into array
		exonic_region_split = exonic_region[:-1].split("\t")

		# get chromosome, start, and end for exonic region
		exonic_region_chromosome = int(exonic_region_split[EXONIC_INDEX_CHROMOSOME])
		exonic_region_start = int(exonic_region_split[EXONIC_INDEX_START])
		exonic_region_end = int(exonic_region_split[EXONIC_INDEX_END])

		if current_variant_chromosome > exonic_region_chromosome:
			continue

		# until we reach the end of this chromosome in the variant file
		while current_variant_chromosome == exonic_region_chromosome:

			if(current_variant_location >= exonic_region_start) & (current_variant_location <= exonic_region_end):
				# Variant is in chromosome, and in exonic region.
				print current_variant_line

				# UNCOMMENT THE BELOW LINE TO PRINT THE REGION IT WAS FOUND IN
				#print exonic_region

			elif current_variant_location > exonic_region_end:
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

if __name__ == "__main__":
	check_exon_function()
