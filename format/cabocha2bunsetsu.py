from __init__ import *
from cabocha2snt import INFO

def output(bunsetsu):
    if bunsetsu:
        sys.stdout.write('\t'.join((
            options.delimiter.join(map(itemgetter(0),bunsetsu)),
            options.delimiter.join(map(itemgetter(1),bunsetsu)),)))
    sys.stdout.write(linesep)

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--delimiter", dest="delimiter", help="morph delimeter", default="")
    options, args = parser.parse_args()
    bunsetsu = []
    for line in imap(str.strip, sys.stdin):
        if not line:
            output(bunsetsu)
            bunsetsu = []
            sys.stdout.write(linesep)
            continue
        bInfo = INFO.match(line)
        if bInfo:
            if bunsetsu:
                output(bunsetsu)
            bunsetsu = []
            chunkno, governor, head_start, head_end = map(int, bInfo.groups())
            i = 0
        else:
            morph, pos = line.split('\t')
            if head_start == i:
                bunsetsu.append((morph, pos))
            elif head_start < i <= head_end:
                bunsetsu.append((morph, morph))
            else:
                bunsetsu.append((morph, ""))
            i += 1
