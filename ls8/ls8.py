#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) == 2:
    cpu = CPU()
    # filename = sys.argv[1]
    cpu.load(sys.argv[1])
    cpu.run()
else:
    print("not possible")