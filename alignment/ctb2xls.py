import sys, re
from os import linesep
import xlwt, arial10, math

if len(sys.argv) < 2:
    sys.stderr.write("usage: python ctb2xls.py xls < ctb"+linesep)
    sys.exit(1)

wb = xlwt.Workbook(encoding="utf-8")
pstyle = xlwt.easyxf("font: color green; align: horiz center")
sstyle = xlwt.easyxf("font: color blue; align: horiz center")

k = 0
row = 0
SOURCE=re.compile("^<source>(.*)</source>$")
TRANSLATION=re.compile("^<translation>(.*)</translation>$")
for line in map(str.strip, sys.stdin):
	if line.startswith("<seg"):
		k += 1
		ws = wb.add_sheet(str(k), cell_overwrite_ok=True)
		ws.set_panes_frozen(True) # frozen headings instead of split panes
		ws.set_horz_split_pos(1)
		ws.set_vert_split_pos(1)		    
		ws.write(0, 1, "NULL")
		ws.write(1, 0, "NULL")
	if SOURCE.match(line):
		source = SOURCE.match(line).group(1)
		for j, fj in enumerate(source.split(), 2):
		    ws.write(0, j, fj)
		    ws.col(j).width = int(math.ceil(arial10.fitwidth(fj)))
	elif TRANSLATION.match(line):
		translation = TRANSLATION.match(line).group(1)
		for i, ei in enumerate(translation.split(), 2):
		    ws.write(i, 0, ei)
	elif line == "<matrix>":
		row = 1
	elif line == "</matrix>":
		row = 0
	elif row > 0:
		for col, aj in enumerate(line.split(),1):
			if aj == '1':
				ws.write(row, col, "S", sstyle)
		row += 1
wb.save(sys.argv[1])
