from __init__ import *

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--delimiter", dest="delimiter", help="delimiter in a chunk", default=" ")
    options, args = parser.parse_args()
    for line in sys.stdin:
        i = count(0)
        while line.strip():
            chunkno = i.next()
            for t in zip(*map(lambda s: s.split(options.delimiter), line.strip().split('\t'))):
                sys.stdout.write('\t'.join(map(str,t+(chunkno,))))
                sys.stdout.write(linesep)
            line = sys.stdin.next()
        sys.stdout.write(linesep)
