#!/bin/bash

. assert.sh

# Version 1.1.0
#$ zcat Proj_06721_C_HaplotypeCaller__FixMulti___v1.1.0.vcf.gz | md5sum -
#    a40833c0400b33b61ceb2ebba6123f4d  -

# Version 2.0.1
#$ zcat Proj_06721_C_HaplotypeCaller__FixMulti___v2.0.1.vcf.gz | md5sum -
#    9c24d5ca1f6bed02bf4c9e79cdf703b5  -

# Newest commit 
# zcat files/Proj_06721_C_HaplotypeCaller__FixMulti___current.vcf.gz | md5sum -
#    7cc0cf33e1c0f60abcd1cb7b2bfe2769  -


../fixMultiInDel.sh \
    <(zcat files/Proj_06721_C_HaplotypeCaller__MultiOnly.vcf.gz ) \
    Proj_06721_C_HaplotypeCaller__FixMulti.vcf 2> stderr.log

assert \
    "md5sum Proj_06721_C_HaplotypeCaller__FixMulti.vcf | awk '{print \$1}'" \
    7cc0cf33e1c0f60abcd1cb7b2bfe2769

assert_end
