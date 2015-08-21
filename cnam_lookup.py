#!/usr/bin/env python3
# (simplest ever) CNAM Lookup script
# Author: Jack Rosenthal, Steamboat Networks
#
# Usage:
# cd to the directory the script is located
# python3 cnam_lookup.py [11 digit number]
# Call with no arguments to be prompted for a number
import sys
from tscquery import cnam_query
try:
    tn = sys.argv[1]
except:
    tn = input("tn = ")
print(cnam_query(tn).name)
