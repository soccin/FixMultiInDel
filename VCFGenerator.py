import sys
import csv

"""
# Lightweight VCF reader

Python interator class to read VCF as 
a csv (tab-delim) stream. Object variable
`self.header` contains the VCF header while
`self.cHeader` is the csv fieldnames, with
`#CHROM` replaced by `CHROM`
"""

class VCFGenerator:
	def __init__(self, fp):
		self.fp=fp
		self.header=[]
		for line in self.fp:
			self.header.append(line.strip())
			if line.startswith("#CHROM"):
				break
		self.cHeader=self.header[-1].split("\t")
		self.cHeader[0]=self.cHeader[0][1:]
		self.cin=csv.DictReader(fp,
			fieldnames=self.cHeader,
			delimiter="\t",
			)

	def __iter__(self):
		return self


	def next(self):
		r=self.cin.next()
		return r

