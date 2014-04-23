import sys
from os import linesep

def head(input):
    for i, line in enumerate(input):
        while line.strip():
            sys.stdout.write(line)
            try:
                line = input.next()
            except StopIteration:
                break
        sys.stdout.write(linesep)
        if i >= int(options.n)-1:
            return

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog files or < file")
    parser.add_option("-n", "", dest="n", help="the number of head document", default=10)
    options, args = parser.parse_args()
    assert int(options.n)

    if not args:
        head(sys.stdin)
    if args:
        for f in map(open, args):
            if len(args) > 1:
                sys.stdout.write("==> %s <=="%f.name + linesep)
            head(f)
            f.close()
