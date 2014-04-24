import sys, xlrd, xlwt, math, arial10
from os import linesep

if len(sys.argv) < 3:
    sys.stderr.write("usage: python split.py xls num_parts"+linesep)
    sys.exit(1)
wb = xlrd.open_workbook(sys.argv[1])
pstyle = xlwt.easyxf("font: color green; align: horiz center")
sstyle = xlwt.easyxf("font: color blue; align: horiz center")
num_sheets = int(math.ceil(float(wb.nsheets) / int(sys.argv[2])))
sys.stderr.write(("Total %d sentences <= %d sentences * %d parts" %
        (wb.nsheets, num_sheets, int(sys.argv[2]))+linesep))
prefix = ".".join(sys.argv[1].split(".")[:-1])

j = 0
out = xlwt.Workbook(encoding=wb.encoding)
for i, ws in enumerate(wb.sheets(),1):
    wsout = out.add_sheet(ws.name)
    wsout.set_panes_frozen(True) # frozen headings instead of split panes
    wsout.set_horz_split_pos(1)
    wsout.set_vert_split_pos(1)
    for row in range(ws.nrows):
        for col in range(ws.ncols):
            c = ws.cell(row,col).value
            if row == 0 and col > 0:
                wsout.col(col).width = \
                        int(math.ceil(arial10.fitwidth(c.encode("utf-8"))))
            if c == 'S':
                wsout.write(row,col, c, sstyle)
            elif c == 'P':
                wsout.write(row,col, c, pstyle)
            else:
                wsout.write(row,col, c)
    if i % num_sheets == 0:
        sys.stderr.write(("save %s.%d.xls (~%d)" % (prefix, j, i))+linesep)
        out.save("%s.%d.xls" % (prefix, j)) 
        j += 1
        out = xlwt.Workbook(encoding=wb.encoding)

if i % num_sheets != 0:
    sys.stderr.write(("save %s.%d.xls" % (prefix, j))+linesep)
    out.save("%s.%d.xls" % (prefix, j)) 
