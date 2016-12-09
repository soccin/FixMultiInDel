#!/usr/bin/env python2.7

import sys
from VCFGenerator import VCFGenerator

fp=open(sys.argv[1])

vcf=VCFGenerator(fp)

#lineterminator="\n"

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
			elif ref.endswith(alt[1:]):
				delta=len(ref)-len(alt)+1
				print ".",ref[:delta]
				print ".",alt[0]+" "*(delta-1)+alt[1:]
				print v["CHROM"],pos,ref[:delta],alt[0]
				print

			else:
				print >>sys.stderr,"ComplexDeletion", ref, ">", alt, 
				raise ValueError("ComplexDEL %s:%s" %(v["CHROM"],pos))
