import sys
from os import linesep

def tail(input):
    buffer = []
    for line in input:
        sentence = []
        while line.strip():
            sentence.append(line.rstrip())
            try:
                line = input.next()
            except StopIteration:
                break
        buffer.append(sentence)
        if len(buffer) > int(options.n):
            buffer.pop(0)
    for sentence in buffer:
        for line in sentence:
            sys.stdout.write(line + linesep)
        sys.stdout.write(linesep)


if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog files or < file")
    parser.add_option("-n", "", dest="n", help="the number of tail document", default=10)
    options, args = parser.parse_args()
    assert int(options.n)

    if not args:
        tail(sys.stdin)
    if args:
        for f in map(open, args):
            sys.stdout.write("==> %s <=="%f.name + linesep)
            tail(f)
            f.close()

