import sys, re
from os import linesep, SEEK_CUR
BOS = re.compile("<sentence id=(\d+) k=(\d)+ logProb=.+ prob=(.+)>")
EOS = re.compile("</sentence>")
id = None
for line in sys.stdin:
    metainfo = BOS.match(line)
    if metainfo:
        if id and metainfo.group(1) != id:
            sys.stdout.write(linesep)
        id, k, prob = metainfo.groups()
    sys.stdout.write(line)
sys.stdout.write(linesep)
