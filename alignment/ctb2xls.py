#!/usr/bin/python
import sys, re
from os import linesep
import xlwt, arial10, math
from itertools import imap

if len(sys.argv) < 2:
    sys.stderr.write("usage: python ctb2xls.py xls [seg] < ctb"+linesep)
    sys.exit(1)

segfile = None
if len(sys.argv) > 2:
	segfile = open(sys.argv[2])

wb = xlwt.Workbook(encoding="utf-8")
pstyle = xlwt.easyxf("font: color green; align: horiz center")
sstyle = xlwt.easyxf("font: color blue; align: horiz center")

k = 0			# 1-based
row = 0			# 1-based
fstart = 2		# 0 and 1 is reserved for target words and NULL
estart = 2		# 0 and 1 is reserved for source words and NULL
if segfile:
	estart = 3	# 2 is reserverd for word boundary information
SOURCE=re.compile("^<source>(.*)</source>$")
TRANSLATION=re.compile("^<translation>(.*)</translation>$")
for line in imap(str.strip, sys.stdin):
	if line.startswith("<seg"):
		k += 1
		ws = wb.add_sheet(str(k), cell_overwrite_ok=True)
		ws.set_panes_frozen(True) # frozen headings instead of split panes
		ws.set_vert_split_pos(fstart-1)		    
		ws.set_horz_split_pos(estart-1)
		ws.write(0, fstart-1, "NULL")
		ws.write(estart-1, 0, "NULL")
		ws.col(fstart-1).width = int(math.ceil(arial10.fitwidth("NULL")))
	if SOURCE.match(line):
		source = SOURCE.match(line).group(1)
		for j, fj in enumerate(source.split(), fstart):
		    ws.write(0, j, fj)
		    ws.col(j).width = int(math.ceil(arial10.fitwidth(fj)))
		# annotate word boundary as well
		if segfile:
			for seg in imap(str.strip, segfile):
				count = 0
				for fj in source.split():
					if fj in seg:
						count += 1
				#TODO: Levenshtein distance?
				if float(count) / len(source.split()) > 0.5:
					break
			buf = []
			for word in seg.split():
				for i, uch in enumerate(unicode(word, "utf-8")):
					if i == 0:
						buf.append("B")
					else:
						buf.append("I")
			if len(buf) != len(source.split()):
				sys.stderr.write("Mismatch" + linesep)
				sys.stderr.write(seg + linesep)
				sys.stderr.write(source + linesep)
				sys.stderr.write(" ".join(buf) + linesep)
				for fj, bi in zip(source.split(),buf):
					sys.stderr.write(fj+ "/" + bi + linesep)
			for j, fj in enumerate(buf, fstart):
				ws.write(1, j, fj)						
	elif TRANSLATION.match(line):
		translation = TRANSLATION.match(line).group(1)
		for i, ei in enumerate(translation.split(), estart):
		    ws.write(i, 0, ei)
	elif line == "<matrix>":
		row = estart-1
	elif line == "</matrix>":
		row = 0
	elif row > 0:
		for col, aj in enumerate(line.split(),fstart-1):
			if aj == '1':
				ws.write(row, col, "S", sstyle)
		row += 1
		
wb.save(sys.argv[1])
if segfile:
	segfile.close()
