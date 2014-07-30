#!/usr/bin/python
import sys
from os import linesep
import xlrd

if len(sys.argv) < 5:
    sys.stderr.write("usage: python convert-template.py xls source target sure possible [source word boundary]"+linesep)
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

def cell2str(cell):
    c = cell.value
    if type(c) != type(u''):
        c = unicode("{0}".format(c), "utf-8")
    return c.encode("utf-8")

for ws in wb.sheets():
    malformd = False
    for j in range(fstart, ws.ncols):
        if not ws.cell(0,j).value:
            sys.stderr.write("Malformed source @ " + ws.name + linesep)
            malformd = True
            break
    for i in range(estart, ws.nrows):
        if not ws.cell(i,0).value:
            sys.stderr.write("Malformed target @ " + ws.name + linesep)
            malformd = True
            break
    if malformd:
        continue
    f.write(" ".join(map(cell2str, [ws.cell(0,j) \
            for j in range(fstart,ws.ncols)]))+linesep)
    e.write(" ".join(map(cell2str, [ws.cell(i,0) \
            for i in range(estart,ws.nrows)]))+linesep)
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
   	    fwb.write(" ".join(map(cell2str, [ws.cell(1,j) \
            for j in range(fstart,ws.ncols)]))+linesep)
map(file.close, (f,e,s,p))
if fwb:
	fwb.close()
