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
# Haplotype does not set the correct FORMAT
# header for AD
#
#    FORMAT=<ID=AD,Number=.,
#
# needs to be changed to
#
#    FORMAT=<ID=AD,Number=R,
#
# for the splitter to correctly reassign AD but
# then need to undo this for downstream steps to work
#
# Also need to sort VCF since normalize will change
# position of SNP's when it de-pads them.
#

cat $HVCF \
    | sed 's/FORMAT=<ID=AD,Number=.,/FORMAT=<ID=AD,Number=R,/' \
    | bcftools norm -m- \
    | $SDIR/bin/normalizeInDels.py \
    | bedtools sort -i - -header \
    | sed 's/FORMAT=<ID=AD,Number=R,/FORMAT=<ID=AD,Number=.,/' \
    > $OUTFILE

