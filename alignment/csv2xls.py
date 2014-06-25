#!/usr/bin/python
import sys
from os import linesep
import xlwt, arial10, math

if len(sys.argv) < 2:
    sys.stderr.write("usage: python csv2xls.py output < csv"+linesep)
    sys.exit(1)

wb = xlwt.Workbook(encoding="utf-8")
pstyle = xlwt.easyxf("font: color green; align: horiz center")
sstyle = xlwt.easyxf("font: color blue; align: horiz center")

fstart = 2
estart = 2
ID, F, E, S, P = 0, 1, 2, 3, 4
for k, line in enumerate(sys.stdin,1):
    lines = line.split("\t")
    ws = wb.add_sheet(str(k), cell_overwrite_ok=True)
    ws.set_panes_frozen(True) # frozen headings instead of split panes
    ws.set_horz_split_pos(estart-1)
    ws.set_vert_split_pos(fstart-1)
    ws.write(0, 0, "ID="+lines[ID])
    ws.write(0, fstart-1, "NULL")
    ws.write(estart-1, 0, "NULL")
    ws.col(fstart-1).width = int(math.ceil(arial10.fitwidth("NULL")))
    for j, fj in enumerate(lines[F].split(), fstart):
        ws.write(0, j, fj)
        ws.col(j).width = int(math.ceil(arial10.fitwidth(fj)))
    for i, ei in enumerate(lines[E].split(), estart):
        ws.write(i, 0, ei)
    if len(lines) > P: # possible
        for ji in lines[P].split():
            col, row = map(int, ji.split("-"))
            ws.write(row+estart, col+fstart, "P", pstyle)
    if len(lines) > S: # sure (overwrite possible)
        for ji in lines[S].split():
            col, row = map(int, ji.split("-"))
            ws.write(row+estart, col+fstart, "S", sstyle)
wb.save(sys.argv[1])
