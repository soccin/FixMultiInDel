#!/usr/bin/env python2.7

import sys

for line in sys.stdin:
    if not line.startswith("#"):
        F=line.strip().split("\t")
        if F[4].find(",")==-1:
            continue

    print line,
