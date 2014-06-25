#!/usr/bin/python
import sys, xlrd, xlwt, math, arial10
from os import path, linesep

if len(sys.argv) < 3:
    sys.stderr.write("usage: python merge.py output xls+ < id"+linesep)
    sys.exit(1)

istyle = xlwt.easyxf("font: color red; align: horiz left")
pstyle = xlwt.easyxf("font: color green; align: horiz center")
sstyle = xlwt.easyxf("font: color blue; align: horiz center")

out = None
for wb in map(xlrd.open_workbook, sys.argv[2:]):
    if out is None: # for wb.encoding
        out = xlwt.Workbook(encoding=wb.encoding)
    for ws in wb.sheets():
        for i in sys.stdin:
            break
        wsout = out.add_sheet(ws.name)
        wsout.set_panes_frozen(True) # frozen headings instead of split panes

        wsout.set_horz_split_pos(1)
        wsout.set_vert_split_pos(1)
        for row in range(ws.nrows):
            for col in range(ws.ncols):
                c = ws.cell(row,col).value
                if row == 0 and col == 0 and not c:
                    wsout.write(0,0, u"ID="+i.strip(), istyle)
                    continue
                if row == 0 and col > 0:
                    wsout.col(col).width = \
                            int(math.ceil(arial10.fitwidth(c.encode("utf-8"))))
                if c == 'S':
                    wsout.write(row,col, c, sstyle)
                elif c == 'P':
                    wsout.write(row,col, c, pstyle)
                else:
                    wsout.write(row,col, c)
out.save(sys.argv[1])
