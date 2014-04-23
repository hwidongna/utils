import sys, xlrd, xlwt, math, arial10
from os import path

if len(sys.argv) < 3:
    sys.stderr.write("usage: python split.py xls num_parts"+linesep)
    sys.exit(1)
wb = xlrd.open_workbook(sys.argv[1])
pstyle = xlwt.easyxf("font: color green; align: horiz center")
sstyle = xlwt.easyxf("font: color blue; align: horiz center")
num_sheets = int(math.ceil(float(len(wb.sheets())) / int(sys.argv[2])))
prefix = ".".join(path.basename(sys.argv[1]).split(".")[:-1])

j = 0
out = xlwt.Workbook(encoding=wb.encoding)
for i, ws in enumerate(wb.sheets(),1):
    if i % num_sheets == 0:
        out.save("%s.%d.xls" % (prefix, j)) 
        j += 1
        out = xlwt.Workbook(encoding=wb.encoding)
    wsout = out.add_sheet(ws.name)
    wsout.set_panes_frozen(True) # frozen headings instead of split panes
    wsout.set_horz_split_pos(1)
    wsout.set_vert_split_pos(1)
    for row in range(ws.nrows):
        for col in range(ws.ncols):
            c = ws.cell(row,col)
            if row == 0 and col > 0:
                wsout.col(col).width = \
                        int(math.ceil(arial10.fitwidth(c.value.encode("utf-8"))))
            if c.value == 'S':
                wsout.write(row,col, c.value, sstyle)
            elif c.value == 'P':
                wsout.write(row,col, c.value, pstyle)
            else:
                wsout.write(row,col, c.value)

if (i-1) % num_sheets != 0:
    out.save("%s.%d.xls" % (prefix, j)) 
