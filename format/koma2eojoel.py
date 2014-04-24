import sys, re
from os import linesep
KOMAMORPH = re.compile("([^ ]+?)\([A-Za-z0-9]*\)")

if __name__=="__main__":
    for line in sys.stdin:
        while line.strip():
#            sys.stderr.write(line)
#            sys.stderr.write(str(line.strip().split(" : "))+linesep)
            eojeol, morphs = line.strip().split(' : ')
            sys.stdout.write(eojeol.rstrip() + '\t')
            sys.stdout.write(' '.join(KOMAMORPH.findall(morphs)))
            sys.stdout.write(linesep)
            line = sys.stdin.next()
        sys.stdout.write(linesep)
