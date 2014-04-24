from __init__ import *
KOMAMORPH = re.compile("( )?([^ ]+?)/([^ ]+)")

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d", "--delimiter", dest="delimiter", help="morph delimeter", default="")
    options, args = parser.parse_args()
    for line in sys.stdin:
        while line.strip():
            index, head, eojeol, morphs  = map(str.rstrip, line.split('\t'))
            eojeolmorphs, eojeolpos = zip(*map(itemgetter(1,2), KOMAMORPH.findall(morphs)))
            sys.stdout.write("\t".join(
                map(str, map(lambda x:x-1, map(int,(index, head))))+
                map(lambda l: options.delimiter.join(l), (eojeolmorphs, eojeolpos))
                ))
            sys.stdout.write(linesep)
            line = sys.stdin.next()
        sys.stdout.write(linesep)
