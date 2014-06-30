#!/usr/bin/python
import sys

encoding = "utf-8"
if len(sys.argv) > 1:
	encoding = sys.argv[1]
	
total = 0
for line in sys.stdin:
	total += len(unicode(line, encoding))
	
print total
