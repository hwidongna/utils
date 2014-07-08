import sys
from os import linesep
import xlrd

from optparse import OptionParser
parser = OptionParser(usage="usage: %prog [options] xls")
parser.add_option("-f", "--field", dest="field", help="field number (ordered)")
parser.add_option("", "--output-delimiter", dest="delimiter", default="\t", help="output delimiter default is <TAB>")
options, args = parser.parse_args()

if len(args) < 1:
    parser.print_help()
    sys.exit(1)

d = {}
for line in open(args[0]):
    key, value = line.split()
    d[key] = value

for line in sys.stdin:
    for k, v in d.iteritems():
        line = line.replace(k,v)
    sys.stdout.write(line)
