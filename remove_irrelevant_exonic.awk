# This awk program removes anything except field 3, 5 and 6 from the exonic region file.
# It also removes the prefix "chr" from the chromosome field. I.e. chr12 -> 12. This is so the exonic region file can be sorted by chromosome.

match($3, "[0-9]+"){
	if(length(substr($3, RSTART, RLENGTH))<= 2){
			print substr($3, RSTART, RLENGTH) chromosome "\t" $5 "\t" $6
		}
}

