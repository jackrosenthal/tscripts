#!/usr/bin/env python3
# Least Cost Routing Lookup Script
# Author: Jack Rosenthal, Steamboat Networks
# Run with no options for help.
#
# License: If you modify this script, be sure to share the
# source with others and retain attribution to the original
# author. So as long as you do that, free use is granted.
import sqlite3 as sq
import sys
from tscquery import lrn_query

# Option parser
from optparse import OptionParser, OptionGroup

oparse = OptionParser(version="dev v0.00")

ropts = OptionGroup(oparse, "Required Options")

ropts.add_option("-t", "--tn", dest="tn", help="set tn to TN", metavar="TN")
ropts.add_option("-o", "--out", dest="out", help="output format to FORMAT, valid options are pretty and bestcarrier", metavar="FORMAT", default="pretty")
oparse.add_option("-a", "--ani", dest="ani", help="set ani to TN", metavar="TN")
oparse.add_option_group(ropts)

oparse.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="be very verbose")
oparse.add_option("--db", dest="db", default="lcr.db", metavar="FILE", help="Use the database specified by FILE, defaults to lcr.db")

(options, args) = oparse.parse_args()

# Print help if tn not specified
if options.tn is None:
    oparse.print_help()
    sys.exit(0)

# Connect to database
con = sq.connect(options.db)
c = con.cursor()

# Make the lrn query, we will assume that we want extended information. If you don't want to
# spend the extra money on extended information, change extended to False and modify the
# script to choose either interstate or intrastate at guess
query = lrn_query(tn=options.tn, ani=options.ani, extended=True)
c.execute(("select * from lcr where " + ''.join("match = '%s' or " for _x in range(len(query.lrn))) + "0") % \
        tuple(query.lrn[:i+1] for i in range(len(query.lrn)))) # Yes, sort of a hack...

# Copy database cursor results to a list, we are done with the database now.
rtlist = list(c)
con.commit()
c.close()

# Calculate best cost and sort routes
routes = {row[0]: [] for row in rtlist}
for row in rtlist:
    routes[row[0]].append(list(row))
cost_index = 3 if query.intrastate else 2 # intrastate is in row 3 of the database
best_cost = float('inf')
for key, val in routes.items():
    routes[key] = sorted(routes[key], key= lambda i:-len(i[1]))[0]
    if routes[key][cost_index] < best_cost:
        best_cost = routes[key][cost_index]
        best_carrier = key

# Two output routines are available, the first, pretty, gives you a nicely formatted table
# with all the carriers the call can route on and their cost. The second, bestcarrier, will
# simply print the most cost effective carrier. The second is probally better for asterisk
# or your scripts, whereas the first is simply just useful information to you.
if options.out == "pretty":
    print("{: <15} {: <11} {: <8} {: <8}".format("Carrier", "Match", "Inter", "Intra"))
    print("{:-<15} {:-<11} {:-<8} {:-<8}".format("-", "-", "-", "-"))
    for key, val in routes.items():
        print("{: <15} {: <11} {: <8} {: <8}".format(*val))
elif options.out == "bestcarrier":
    print(best_carrier)
