#!/bin/bash
SDIR="$( cd "$( dirname "$0" )" && pwd )"

NORM_EXTRA_OPTS=""

NUMARGS=$#

if [ $NUMARGS -lt 1 ] || [ $NUMARGS -gt 3 ]; then
    echo
    echo "ERROR: Too many/few arugments"
    echo "usage: fixMultiInDel.sh [-a]  INPUT_VCF [OUTPUT_VCF]"
    echo " -a : output all variants when fixing multi indels"
    echo
    exit
fi

while getopts :a FLAG; do
    case $FLAG in
        a)
          NORM_EXTRA_OPTS="-a"
          ;;
        \?) #unrecognized option
          echo
          echo "ERROR: Unrecognized arugment: $OPTARG"
          echo "usage: fixMultiInDel.sh [-a]  INPUT_VCF [OUTPUT_VCF]"
          echo " -a : output all variants when fixing multi indels"
          echo
          exit
          ;;
    esac
done

shift $((OPTIND-1))

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
    echo "ERROR: Cannot find input file in command line"
    echo "usage: fixMultiInDel.sh -a INPUT_VCF [OUTPUT_VCF]"
    echo " -a : output all variants when fixing multi indels"
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
    | $SDIR/bin/normalizeInDels.py $NORM_EXTRA_OPTS \
    | bedtools sort -i - -header \
    | sed 's/FORMAT=<ID=AD,Number=R,/FORMAT=<ID=AD,Number=.,/' \
    > $OUTFILE

