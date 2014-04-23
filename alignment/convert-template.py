import sys
from os import linesep
import xlrd

if len(sys.argv) < 5:
    sys.stderr.write("usage: python convert-template.py xls source target sure possible"+linesep)
    sys.exit(1)

wb = xlrd.open_workbook(sys.argv[1])
f, e, s, p = map(lambda name:open(name, "w"), sys.argv[2:])

for ws in wb.sheets():
    f.write(" ".join([ws.cell(0,j).value.encode("utf-8") \
            for j in range(2,ws.ncols)])+linesep)
    e.write(" ".join([ws.cell(i,0).value.encode("utf-8") \
            for i in range(2,ws.nrows)])+linesep)
    sure, possible = [], []
    for i in range(2, ws.nrows):
        for j in range(2, ws.ncols):
            if ws.cell(i,j).value == 'S':
                sure.append("%d-%d" % (j-2,i-2))
                possible.append("%d-%d" % (j-2,i-2))
            elif ws.cell(i,j).value == 'P':
                possible.append("%d-%d" % (j-2,i-2))
    s.write(" ".join(sure)+linesep)
    p.write(" ".join(possible)+linesep)
map(file.close, (f,e,s,p))
