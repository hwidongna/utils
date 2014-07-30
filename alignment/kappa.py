#!/usr/bin/python
import sys, xlrd, xlwt, math, arial10
from os import path, linesep

if len(sys.argv) < 3:
    sys.stderr.write("usage: python kappa.py xls1 xls2 (xls1 xls2)*"+linesep)
    sys.exit(1)
    
tt, tf, ft, ff = 0, 0, 0, 0
i = 2
while i < len(sys.argv):
    wb1 = xlrd.open_workbook( sys.argv[i-1] )
    wb2 = xlrd.open_workbook( sys.argv[i] )

    if wb1.nsheets != wb2.nsheets:
        sys.stderr.write("Different total # of sentences: {0} != {1}".format(
                            wb1.nsheets, wb2.nsheets)+linesep)
        sys.exit(1)    
        
    for (ws1, ws2) in zip(wb1.sheets(), wb2.sheets()):
        if ws1.name != ws2.name:
            sys.stderr.write("Different sheet name: {0} != {1}".format(
                ws1.name, ws2.name) + linesep)
            continue
        if ws1.ncols != ws2.ncols:
            sys.stderr.write("Different # of source words: {0} != {1} @ {2}".format(
                                ws1.ncols, ws2.ncols, ws1.name)+linesep)
            continue
        if ws1.nrows != ws2.nrows:
            sys.stderr.write("Different # of target words: {0} != {1} @ {2}".format(
                                ws1.nrows, ws2.nrows, ws1.name)+linesep)
            continue
        # True if (target[row],source[col]) is aligned
        # False if (NULL,source[col]) or (target[row],NULL)
        for row in range(2,ws1.nrows):
            c1 = ws1.cell(row,1).value
            c2 = ws2.cell(row,1).value
            if c1 and c2:
                ff += 1
        for col in range(2,ws1.ncols):
            c1 = ws1.cell(1,col).value
            c2 = ws2.cell(1,col).value
            if c1 and c2:
                ff += 1
        for row in range(2,ws1.nrows):
            for col in range(2,ws1.ncols):
                c1 = ws1.cell(row,col).value
                c2 = ws2.cell(row,col).value
                if not c1 and not c2:
                    continue
                elif not c1:
                    tf += 1
                elif not c2:
                    ft += 1                
                else: # if c1 and c2:
                    tt += 1
    # end for
    i += 2
# end while
total = tt + tf + ft + ff
pa = float(tt + ff)/total
pe = float(tt + tf)/total * float(tt + ft)/total \
    +float(ff + tf)/total * float(ff + ft)/total
sys.stdout.write( "{0}\t{1}".format( tt, tf ) + linesep)
sys.stdout.write( "{0}\t{1}".format( ft, ff ) + linesep)
sys.stdout.write( "Kappa: {0:.4f}".format( (pa-pe) / (1-pe) ) + linesep)
