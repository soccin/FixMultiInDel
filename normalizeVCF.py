#!/usr/bin/env python2.7

import sys
import csv
from VCFGenerator import VCFGenerator

fp=open(sys.argv[1])

vcf=VCFGenerator(fp)

#lineterminator="\n"

cout=csv.DictWriter(
	sys.stdout,
	vcf.cHeader,
	delimiter="\t",
	lineterminator="\n")

for v in vcf:
	ref=v["REF"]
	alt=v["ALT"]
	pos=int(v["POS"])
	if len(ref)>1 and len(alt)>1:
		print v["CHROM"],v["POS"],v["REF"],v["ALT"]
		if len(ref)>len(alt):
			# Deletion
			print " ",ref
			if ref.startswith(alt):
				delta=len(alt)-1
				print " "*(delta+1),ref[delta:]
				print " "*(delta+1),alt[delta:]
				print v["CHROM"],pos+delta,ref[delta:],alt[delta:]
				print

				v["POS"]=pos+delta
				v["REF"]=ref[delta:]
				v["ALT"]=alt[delta:]

			elif ref.endswith(alt[1:]):
				delta=len(ref)-len(alt)+1
				print ".",ref[:delta]
				print ".",alt[0]+" "*(delta-1)+alt[1:]
				print v["CHROM"],pos,ref[:delta],alt[0]
				print

				v["REF"]=ref[:delta]
				v["ALT"]=alt[0]

			else:
				print >>sys.stderr,"ComplexDeletion", ref, ">", alt, 
				raise ValueError("ComplexDEL %s:%s" %(v["CHROM"],pos))

			v["ID"]="DEL"
			print v["CHROM"],v["POS"],v["REF"],v["ALT"],"FIX"

	cout.writerow(v)
