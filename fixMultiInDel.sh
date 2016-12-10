#!/bin/bash
SDIR="$( cd "$( dirname "$0" )" && pwd )"

case $# in
    2)
    HVCF=$1
    OUTFILE=$2
    ;;

    1)
    HVCF=$1
    OUTFILE=$(basename $HVCF | sed 's/.vcf$/___FixInDels.vcf/')
    ;;

    *)
    echo
    echo "usage: fixMultiInDel.sh INPUT_VCF [OUTPUT_VCF]"
    echo
    exit
    ;;

esac

#
# vcfbreakmulti create ./0 genotypes that
# should be 0/0. Fix them to prevent problems
# downstream

$SDIR/bin/vcfbreakmulti $HVCF \
    | $SDIR/bin/normalizeInDels.py \
    | perl -pe 's|./0|0/0|g' \
    > $OUTFILE

