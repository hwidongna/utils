import sys
from os import linesep

s = set()
for line in sys.stdin:
	if line in s:
		continue
	sys.stdout.write(line)
	s.add(line)
