import sys, xlrd, xlwt, math, arial10
from os import path, linesep

if len(sys.argv) < 3:
    sys.stderr.write("usage: python split.py output input1 input2"+linesep)
    sys.exit(1)

pstyle = xlwt.easyxf("font: color green; align: horiz center")
sstyle = xlwt.easyxf("font: color blue; align: horiz center")
dstyle = xlwt.easyxf("font: color red, struck_out 1; align: horiz center")
istyle = xlwt.easyxf("font: color red; align: horiz center")
wb1, wb2 = map(xlrd.open_workbook, sys.argv[2:])

if wb1.nsheets != wb2.nsheets:
    sys.stderr.write("different # of sheets: %d != %d" % (wb1.nsheets , wb2.nsheets) + linesep)
    sys.exit(1)

out = xlwt.Workbook(encoding=wb1.encoding)
for (ws1, ws2) in zip(wb1.sheets(), wb2.sheets()):
    if ws1.name != ws2.name:
        sys.stderr.write("different sheet name: %s != %s" % (ws1.name, ws2.name) + linesep)
        continue
    if ws1.nrows != ws2.nrows:
        sys.stderr.write("different # rows: %d != %d" % (ws1.nrows, ws2.nrows) + linesep)
        continue
    if ws1.ncols != ws2.ncols:
        sys.stderr.write("different # cols: %d != %d" % (ws1.ncols, ws2.ncols) + linesep)
        continue
    wsout = out.add_sheet(ws1.name)
    
    wsout.set_panes_frozen(True) # frozen headings instead of split panes
    wsout.set_horz_split_pos(1)
    wsout.set_vert_split_pos(1)
    nins, ndel, nsub = 0, 0, 0
    for row in range(ws1.nrows):
        for col in range(ws1.ncols):
            c1 = ws1.cell(row,col).value
            c2 = ws2.cell(row,col).value
            if row == 0 and col > 0:
                wsout.col(col).width = \
                        int(math.ceil(arial10.fitwidth(c1.encode("utf-8"))))
            if c1 == c2:
                if c1 == 'S':
                    wsout.write(row,col, c1, sstyle)
                elif c1 == 'P':
                    wsout.write(row,col, c1, pstyle)
                else:
                    wsout.write(row,col, c1)
            elif len(c1) == 0 and c2: # inserted
                nins += 1
                wsout.write(row,col, c2, istyle)
            elif c1 and len(c2) == 0: # deleted 
                ndel += 1
                wsout.write(row,col, c1, dstyle)
            elif c1 != c2: # substituted
                nsub += 1
                wsout.write(row,col, "%s->%s" %(c1, c2), istyle)
    print nins, ndel, nsub
out.save(sys.argv[1])
