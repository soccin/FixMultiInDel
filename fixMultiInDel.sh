#!/bin/bash
SDIR="$( cd "$( dirname "$0" )" && pwd )"

HVCF=$1

$SDIR/bin/vcfbreakmulti $HVCF \
    | $SDIR/bin/normalizeInDels.py \
    > $(basename $HVCF | sed 's/.vcf$/___FixInDels.vcf/')

