from __init__ import *

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-o", "--original", dest="original", help="Original MST")
    options, args = parser.parse_args()
    original = open(options.original)
    normalized = sys.stdin
    trinity = [original, normalized,]
    while True:
        try:
            oline, pline = map(str.strip, map(file.next,trinity))
        except StopIteration:
            break
        if withlabel(oline):
            sys.stdout.write('\t'.join(oline.split('\t')[:3]+pline.split('\t')[-1:])+linesep)
        else:
            sys.stdout.write('\t'.join(oline.split('\t')[:2]+pline.split('\t')[-2:])+linesep)
    map(file.close, trinity)
