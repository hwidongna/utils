import sys, os, re
from itertools import imap
from os import linesep
INFO = re.compile("\* (\d+) (-1|\d+)[O|D] (\d+)/(\d+)")#* 0 11D 0/0 2.08150609

if __name__=="__main__":
   for line in imap(str.strip, sys.stdin):
        if not line:
            sys.stdout.write(linesep)
            continue
        bInfo = INFO.match(line)
        if bInfo:
            chunkno, governor, head_start, head_end = map(int, bInfo.groups())
            i = 0
            continue
        if i <= head_start:
            sys.stdout.write('\t'.join(line.split('\t')+map(str,[chunkno]))+linesep)
        i += 1
