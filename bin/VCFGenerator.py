import sys
import csv

"""
# Lightweight VCF reader

Python interator class to read VCF as
a csv (tab-delim) stream. Object variable
`self.header` contains the VCF header while
`self.cHeader` is the csv fieldnames
"""

class VCFGenerator:
	def __init__(self, fp):
		self.header=[]
		for line in fp:
			if line.startswith("#CHROM"):
				break
			self.header.append(line.strip())

		self.cHeader=line.strip().split("\t")
		self.cin=csv.DictReader(fp,
			fieldnames=self.cHeader,
			delimiter="\t",
			)

	def __iter__(self):
		return self


	def next(self):
		r=self.cin.next()
		return r

