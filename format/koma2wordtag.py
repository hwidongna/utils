import sys, re
from os import linesep
KOMAMORPH = re.compile("([^ ]+?)\(([A-Za-z0-9\+]+)\)")

if __name__=="__main__":
    for line in sys.stdin:
        id = 0
        while line.strip():
#            sys.stderr.write(line)
#            sys.stderr.write(str(line.strip().split(" : "))+linesep)
            em = line.strip().split(' : ')
            if len(em) == 2:
                eojeol, morphs = em
                for morph in KOMAMORPH.findall(morphs):
                    sys.stdout.write('\t'.join(morph+(str(id),)))
                    sys.stdout.write(linesep)
                id += 1
            line = sys.stdin.next()
        sys.stdout.write(linesep)
