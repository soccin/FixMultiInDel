# FixMultiInDel

Fix problem with VCF calls multiple insertion and/or deletion events at a given position. 
Uses `bcftools norm` to do the splitting.


## Examples:

- From haplotype

```
    5   112174757   .   GAAGA   G,GGA
```

- after bcftools norm -m-

```
    5   112174757   .   GAAGA   G
    5   112174757   .   GAAGA   GGA
```

- after normalizeInDels.py

```
	5	112174757	.	GAAGA	G
	5	112174757	.	GAA		G
```
