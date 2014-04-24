import sys, re
from os import linesep

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] <reference files>...")
    parser.add_option("", "--thresold", dest="thresold", help="prob thresold")
    options, args = parser.parse_args()
    refs = map(open, args)
    refid = -1
    for line in sys.stdin:
        id, k, prob, sent = map(str.strip, line.split('\t'))
        if float(prob) < float(options.thresold):
            continue
        while refid < int(id):
            refsents = []
            for ref in refs:
                refsents.append(ref.next().strip())
            refid += 1
        for refsent in refsents:
            sys.stdout.write("\t".join(map(str,(
                id, k, prob, sent, refsent))) + linesep)
    map(file.close, refs)
