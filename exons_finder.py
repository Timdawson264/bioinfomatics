#!/usr/bin/python2
import sqlite3
import sys

#DEFINES
VARIANT_INDEX_CHROMOSOME = 0
VARIANT_INDEX_LOCATION = 1

if __name__ == "__main__":

  if(len(sys.argv)) != 4:
		print("USAGE: %s exon_file.sqlite variance_file [Assosiatedgenes.txt] " % sys.argv[0])
		sys.exit(1)
  
  conn = sqlite3.connect(sys.argv[1])
  variant_file = open(sys.argv[2])

  gene_file = open(sys.argv[3])
  genes = gene_file.read(-1).split()
  
  # skip title row
  while variant_file.readline()[1]=='#': pass
  
  for var in variant_file:
    
    v = var.split("\t")
    t = (v[VARIANT_INDEX_CHROMOSOME],v[VARIANT_INDEX_LOCATION],v[VARIANT_INDEX_LOCATION])
    for row in conn.execute('select name, name2 from Exons where chrom="chr"||? and  txStart<=? and txEnd>=?', t):
      if(row[1] in genes):
        print row[0], row[1]
        print var
        print

