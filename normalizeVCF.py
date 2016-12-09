#!/usr/bin/env python2.7

import sys
from VCFGenerator import VCFGenerator

fp=open("dat/test.vcf")

vcf=VCFGenerator(fp)

#lineterminator="\n"

for v in vcf:
	ref=v["REF"]
	alt=v["ALT"]
	if len(ref)>1 and len(alt)>1:
		print v["CHROM"],v["POS"],v["REF"],v["ALT"]

#print v
