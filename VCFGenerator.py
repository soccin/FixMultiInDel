import sys
import csv

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

