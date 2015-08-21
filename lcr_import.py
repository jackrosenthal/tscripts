#!/usr/bin/env python3
# LCR Database Import Helper
# Author: Jack Rosenthal, Steamboat Networks
# This script is to help you import CSV files from the carrier
# to your sqlite database
#
# Run with no options for help
#
# License: If you modify this script, be sure to share the
# source with others and retain attribution to the original
# author. So as long as you do that, free use is granted.
import sqlite3 as sq
import csv
import sys

# Option Parser
from optparse import OptionParser, OptionGroup
oparse = OptionParser(version="dev v0.00")
ropts = OptionGroup(oparse, "Required Options")
ropts.add_option("-n", "--name", dest="name", help="set the carrier name to NAME", metavar="NAME")
oparse.add_option_group(ropts)
oparse.add_option("-c", "--csv", dest="csv", help="read dynamic rate table from FILE", metavar="FILE")
oparse.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="be very verbose")
oparse.add_option("-r", "--remove", action="store_true", dest="remove", default=False, help="remove the specified carrier")
oparse.add_option("--db", dest="db", default="lcr.db", metavar="FILE", help="Use the database specified by FILE, defaults to lcr.db")
oparse.add_option("--f-match", type="int", dest="match", metavar="N", help="Use CSV field N for match", default=0)
oparse.add_option("--f-inter", type="int", dest="inter", metavar="N", help="Use CSV field N for interstate rate", default=1)
oparse.add_option("--f-intra", type="int", dest="intra", metavar="N", help="Use CSV field N for intrastate rate", default=2)
(options, args) = oparse.parse_args()

# Functons to print errors and verbose messages
def verb(*objs):
    if options.verbose:
        print("Verbose:", *objs)

def error(*objs):
    print("Error:", *objs, file=sys.stderr)

# Check for sanity, print help if needed
if options.name is None:
    verb("name option was not specified, printing help...")
    oparse.print_help()
    sys.exit(0)

if (options.csv is None) + (options.remove is False) != 1:
    error("Invalid action")
    sys.exit(1)

# Open connection to database
con = sq.connect(options.db)
c = con.cursor()
def sqexec(*objs):
    if options.verbose:
        print("Sql:", *objs)
    c.execute(*objs)
sqexec("CREATE TABLE IF NOT EXISTS main.lcr (carrier TEXT NOT NULL, match TEXT NOT NULL, interstate REAL NOT NULL, intrastate REAL NOT NULL)")

# Add CSV to database
if options.csv is not None:
    with open(options.csv, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            sqexec("INSERT INTO lcr VALUES ('{}', '{}', {}, {})".format(options.name, row[options.match], row[options.inter], row[options.intra]))

# Remove carrier from database
elif options.remove:
    sqexec("DELETE FROM lcr WHERE carrier = '{}'".format(options.name))

# Close connection, Bye!
con.commit()
c.close()
