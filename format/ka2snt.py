from __init__ import *
KOMAMORPH = re.compile("( )?([^ ]+?)/([^ ]+)")

def contain(patterns, string):
    for pattern in patterns:
        if pattern.match(string):
            return True
    return False

def load(filename):
    result = set()
    if filename:
        for line in map(str.rstrip, open(filename)):
            result.add(re.compile(line))
    return result

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a", "--allow", dest="allow", help="allowed POS tag set")
    parser.add_option("-d", "--deny", dest="deny", help="denied POS tag set")
    options, args = parser.parse_args()
    allowed = load(options.allow)
    denied = load(options.deny)
    for line in sys.stdin:
        while line.strip():
            index, head, eojeol, morphs = map(str.rstrip, line.split('\t'))
            for _, morph, tag in KOMAMORPH.findall(morphs):
                if not contain(allowed, "/".join((morph,tag))) or contain(denied, "/".join((morph,tag))):
                    continue
                sys.stdout.write('\t'.join(map(str, (morph, tag, int(index)-1))))
                sys.stdout.write(linesep)
            line = sys.stdin.next()
        sys.stdout.write(linesep)
