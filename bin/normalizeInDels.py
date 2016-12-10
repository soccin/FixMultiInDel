#!/usr/bin/env python2.7

"""
normalizeInDels

Given a VCF in which multi-allelic events have already been
split this script normalize any _padded_ events, i.e.;

Deletion:
	chr1,970549,TGG,TG
	chr1,970550, GG, G

Insertion:
	chr1,4439107,AAGGAGG,AAGGAGGAGG
	chr1,4439113,      G,      GAGG

Since this is for the post processing of in/dels from
haplotypecaller only in/dels are writing out, SNPs (and ONPs)
are filtered out to reduce file size.

"""

import sys
import csv
from VCFGenerator import VCFGenerator

if len(sys.argv)==2:
	fp=open(sys.argv[1])
else:
	fp=sys.stdin

vcf=VCFGenerator(fp)

cout=csv.DictWriter(
	sys.stdout,
	vcf.cHeader,
	delimiter="\t",
	lineterminator="\n")

print "\n".join(vcf.header)
print "##normalizeInDels.py<Version=1.0>"
cout.writeheader()
for v in vcf:
	ref=v["REF"]
	alt=v["ALT"]
	pos=int(v["POS"])
	if len(ref)>1 and len(alt)>1:
		if len(ref)>len(alt):

			# Deletion
			if ref.startswith(alt):
				delta=len(alt)-1
				v["POS"]=pos+delta
				v["REF"]=ref[delta:]
				v["ALT"]=alt[delta:]

			elif ref.endswith(alt[1:]):
				delta=len(ref)-len(alt)+1
				v["REF"]=ref[:delta]
				v["ALT"]=alt[0]

			else:
				print >>sys.stderr,"ComplexDeletion", ref, ">", alt
				raise ValueError("ComplexDEL %s:%s" %(v["#CHROM"],pos))

		elif len(ref)<len(alt):

			# Insertion
			if alt.startswith(ref):
				delta=len(ref)-1
				v["POS"]=pos+delta
				v["REF"]=ref[delta:]
				v["ALT"]=alt[delta:]

			elif alt.endswith(ref[1:]):
				delta=len(alt)-len(ref)+1
				v["REF"]=ref[0]
				v["ALT"]=alt[:delta]

			else:
				print >>sys.stderr,"ComplexInsertion", ref, ">", alt
				raise ValueError("ComplexINS %s:%s" %(v["#CHROM"],pos))


	if len(ref)!=len(alt):
		cout.writerow(v)



