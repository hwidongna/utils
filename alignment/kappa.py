#!/usr/bin/python
import sys, xlrd, xlwt, math, arial10
from os import path, linesep

if len(sys.argv) != 3:
    sys.stderr.write("usage: python kappa.py xls1 xls2"+linesep)
    sys.exit(1)
    
wb1 = xlrd.open_workbook( sys.argv[1] )
wb2 = xlrd.open_workbook( sys.argv[2] )

if wb1.nsheets != wb2.nsheets:
    sys.stderr.write("Different total # of sentences: {0} != {1}".format(
                        wb1.nsheets, wb2.nsheets)+linesep)
    sys.exit(1)    
    
tt, tf, ft, ff = 0, 0, 0, 0
for (ws1, ws2) in zip(wb1.sheets(), wb2.sheets()):
    if ws1.cell(0,0).value != ws2.cell(0,0).value:
        sys.stderr.write("Different ID: {0} != {1}".format(
                            ws1.cell(0,0).value, ws2.cell(0,0).value)+linesep)
        sys.exit(1)
    if ws1.ncols != ws2.ncols:
        sys.stderr.write("Different # of source words: {0} != {1}".format(
                            ws1.ncols, ws2.ncols)+linesep)
        sys.exit(1)
    if ws1.nrows != ws2.nrows:
        sys.stderr.write("Different # of target words: {0} != {1}".format(
                            ws1.nrows, ws2.nrows)+linesep)
        sys.exit(1)
    # True if (target[row],source[col]) is aligned
    # False if (NULL,source[col]) or (target[row],NULL)
    for row in range(1,ws1.nrows):
        for col in range(1,ws1.ncols):
            c1 = ws1.cell(row,col).value
            c2 = ws2.cell(row,col).value
            if not c1 and not c2:
                continue
            elif not c1:
                tf += 1
            elif not c2:
                ft += 1                
            else: # if c1 and c2:
                if row == 1 or col == 1:
                    ff += 1
                else:
                    tt += 1

total = tt + tf + ft + ff
pa = float(tt + ff)/total
pe = float(tt + tf)/total * float(tt + ft)/total \
    +float(ff + tf)/total * float(ff + ft)/total
sys.stdout.write( "{0}\t{1}".format( tt, tf ) + linesep)
sys.stdout.write( "{0}\t{1}".format( ft, ff ) + linesep)
sys.stdout.write( "Kappa: {0:.4f}".format( (pa-pe) / (1-pe) ) + linesep)
