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

fields = map(lambda x:x-1, map(int, options.field.split(",")))

wb = xlrd.open_workbook(args[0])
for ws in wb.sheets():
    sys.stdout.write("# "+ ws.name + linesep)
    for i in range(ws.nrows):
        records = {}
        for j in range(ws.ncols):
            if not fields or j in fields:
                c = ws.cell(i,j)
                if c.ctype in (0,1,6,): # string types
                    records[j] = c.value.encode("utf-8").strip()
                elif c.ctype in (2,3,4,): # number types
                    records[j] = str(c.value)
                else: # error
                    sys.stderr.write("Error at [%d,%d] in %s" % (i,j,ws.name) + linesep)
        sys.stdout.write(options.delimiter.join([records[j] for j in fields]) + linesep)
    sys.stdout.write(linesep)

