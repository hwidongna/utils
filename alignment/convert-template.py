#!/usr/bin/python
import sys
from os import linesep
import xlrd

if len(sys.argv) < 5:
    sys.stderr.write("usage: python convert-template.py xls source target sure possible [source word boundary] > ids"+linesep)
    sys.exit(1)

wb = xlrd.open_workbook(sys.argv[1])
f, e, s, p = map(lambda name:open(name, "w"), sys.argv[2:6])

fwb = None
if len(sys.argv) > 6:
	fwb = open(sys.argv[6], "w")

fstart = 2		# 0 and 1 is reserved for target words and NULL
estart = 2		# 0 and 1 is reserved for source words and NULL
if fwb:
	estart = 3	# 2 is reserverd for word boundary information
for ws in wb.sheets():
    sys.stdout.write(ws.cell(0,0).value.encode("utf-8").replace("ID=","")+linesep)
    f.write(" ".join([ws.cell(0,j).value.encode("utf-8") \
            for j in range(fstart,ws.ncols)])+linesep)
    e.write(" ".join([ws.cell(i,0).value.encode("utf-8") \
            for i in range(estart,ws.nrows)])+linesep)
    sure, possible = [], []
    for i in range(estart, ws.nrows):
        for j in range(fstart, ws.ncols):
            if ws.cell(i,j).value == 'S':
                sure.append("%d-%d" % (j-fstart,i-estart))
                possible.append("%d-%d" % (j-fstart,i-estart))
            elif ws.cell(i,j).value == 'P':
                possible.append("%d-%d" % (j-fstart,i-estart))
    s.write(" ".join(sure)+linesep)
    p.write(" ".join(possible)+linesep)
    if fwb:
   	    fwb.write(" ".join([ws.cell(1,j).value.encode("utf-8") \
            for j in range(fstart,ws.ncols)])+linesep)
map(file.close, (f,e,s,p))
if fwb:
	fwb.close()
