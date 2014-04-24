import sys, re
from os import linesep
from itertools import count

BOS = re.compile("<sentence id=(\d+) k=(\d)+ logProb=.+ prob=(.+)>")
EOS = re.compile("</sentence>")

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] < stanford-seg > id k prob sent")
    parser.add_option("", "--encoding", dest="encoding", help="charater encoding", default="utf-8")
    parser.add_option("-k", "", dest="k", help="the number of difference segmentation for each segnmentation file")
    options, args = parser.parse_args()
    for line in sys.stdin:
        if not line.strip():
            continue
        metainfo = BOS.match(line.strip())
        if metainfo:
            id, k, prob = metainfo.groups()
        elif int(k) > int(options.k):
            continue
        elif not EOS.match(line.strip()):
            sys.stdout.write("\t".join(map( str, (id, k, prob, line.strip()))) + linesep)
