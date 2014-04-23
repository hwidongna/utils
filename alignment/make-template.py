import sys
from os import linesep
import xlwt, arial10, math

if len(sys.argv) < 3:
    sys.stderr.write("usage: python make-template.py output source target [sure] [possible]"+linesep)
    sys.exit(1)

files = map(open, sys.argv[2:])

wb = xlwt.Workbook(encoding="utf-8")
pstyle = xlwt.easyxf("font: color green; align: horiz center")
sstyle = xlwt.easyxf("font: color blue; align: horiz center")

k = 0
while True:
    k += 1
    try:
        lines = map(file.next, files)
    except:
        break
    ws = wb.add_sheet(str(k), cell_overwrite_ok=True)
    ws.set_panes_frozen(True) # frozen headings instead of split panes
    ws.set_horz_split_pos(1)
    ws.set_vert_split_pos(1)
    ws.write(0, 1, "NULL")
    ws.write(1, 0, "NULL")
    ws.col(1).width = int(math.ceil(arial10.fitwidth("NULL")))
    for j, fj in enumerate(lines[0].split(), 2):
        ws.write(0, j, fj)
        ws.col(j).width = int(math.ceil(arial10.fitwidth(fj)))
    for i, ei in enumerate(lines[1].split(), 2):
        ws.write(i, 0, ei)
    if len(lines) > 3: # possible
        for ji in lines[3].split():
            col, row = map(int, ji.split("-"))
            ws.write(row+2, col+2, "P", pstyle)
    if len(lines) > 2: # sure (overwrite possible)
        for ji in lines[2].split():
            col, row = map(int, ji.split("-"))
            ws.write(row+2, col+2, "S", sstyle)
wb.save(sys.argv[1])
map(file.close, files)
