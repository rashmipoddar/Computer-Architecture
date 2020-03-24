#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) == 1:
  print('Please provide the filename')
else:
  filename = sys.argv[1]
  cpu = CPU()
  # cpu.load()
  cpu.load_dynamic(filename)
  cpu.run()


# When running the file while providing the file that has to be used we provide the path
# Run this file by python3 ls8.py examples/print8.ls8
