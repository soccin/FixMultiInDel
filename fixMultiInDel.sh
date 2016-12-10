#!/bin/bash
SDIR="$( cd "$( dirname "$0" )" && pwd )"

case $# in
    2)
    HVCF=$1
    OUTFILE=$2
    ;;

    1)
    HCF=$1
    OUTFILE=$(basename $HVCF | sed 's/.vcf$/___FixInDels.vcf/')
    ;;

    *)
    echo
    echo "usage: fixMultiInDel.sh INPUT_VCF [OUTPUT_VCF]"
    echo
    exit
    ;;

esac

$SDIR/bin/vcfbreakmulti $HVCF \
    | $SDIR/bin/normalizeInDels.py \
    > $OUTFILE

