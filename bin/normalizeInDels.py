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

This could be used in two ways, either to always have all variants 
output or to restrict output to just the INDELs. 

"""
import argparse
import sys
import csv
from VCFGenerator import VCFGenerator


parser = argparse.ArgumentParser(description="Normalizing complex indels after splitting")
parser.add_argument('-i','--inFile',nargs="?",help="Input File", type=argparse.FileType('r'), default=sys.stdin)
parser.add_argument('-o','--out',nargs="?",help="Output File", type=argparse.FileType('w'), default=sys.stdout)
parser.add_argument('-a','--allVars',action='store_true',help="Flag that change output to contain all variants, not just INDELs")
args = parser.parse_args()

fp=args.inFile
vcf=VCFGenerator(fp)

cout=csv.DictWriter(
	args.out,
	vcf.cHeader,
	delimiter="\t",
	lineterminator="\n")

print "\n".join(vcf.header)
print "##normalizeInDels.py=<Version=2.0.1>"
cout.writeheader()
for v in vcf:
	ref=v["REF"]
	alt=v["ALT"]
	pos=int(v["POS"])
	if len(ref)>1 and len(alt)>1:
		if len(ref)>len(alt):

                        # Deletion
                        if ref.endswith(alt[1:]):
                                delta=len(ref)-len(alt)+1
                                v["REF"]=ref[:delta]
                                v["ALT"]=alt[0]

			elif ref.startswith(alt):
				delta=len(alt)-1
				v["POS"]=pos+delta
				v["REF"]=ref[delta:]
				v["ALT"]=alt[delta:]

			else:
				print >>sys.stderr,"ComplexDeletion", ref, ">", alt
				raise ValueError("ComplexDEL %s:%s" %(v["#CHROM"],pos))

		elif len(ref)<len(alt):

			# Insertion
                        
			if alt.endswith(ref[1:]):
				delta=len(alt)-len(ref)+1
				v["REF"]=ref[0]
				v["ALT"]=alt[:delta]

                        elif alt.startswith(ref):
                                delta=len(ref)-1
                                v["POS"]=pos+delta
                                v["REF"]=ref[delta:]
                                v["ALT"]=alt[delta:]

			else:
				print >>sys.stderr,"ComplexInsertion", ref, ">", alt
				raise ValueError("ComplexINS %s:%s" %(v["#CHROM"],pos))

	if args.allVars:
		cout.writerow(v)
	elif len(ref)!=len(alt):
		cout.writerow(v)



