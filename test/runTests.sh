#!/bin/bash

. assert.sh

#$ zcat Proj_06721_C_HaplotypeCaller__FixMulti.vcf.gz | md5sum -
# a40833c0400b33b61ceb2ebba6123f4d  -

../fixMultiInDel.sh \
    <(zcat files/Proj_06721_C_HaplotypeCaller__MultiOnly.vcf.gz ) \
    Proj_06721_C_HaplotypeCaller__FixMulti.vcf 2> stderr.log

assert \
    "md5sum Proj_06721_C_HaplotypeCaller__FixMulti.vcf | awk '{print \$1}'" \
    a40833c0400b33b61ceb2ebba6123f4d

assert_end