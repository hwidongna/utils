import sys
from os import linesep

s = set()
for filename in sys.argv[1:]:
	for line in open(filename):
		s.add(line.strip())

for line in sys.stdin:
	if line.strip() in s:
		continue
	sys.stdout.write(line.strip()+linesep)
	s.add(line.strip())
