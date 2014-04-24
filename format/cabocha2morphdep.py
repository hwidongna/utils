from __init__ import *
from cabocha2snt import INFO

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    options, args = parser.parse_args()
    tree = Tree()
    i = 0
    dependents = {}
    heads = {-1:-1}
    for line in imap(str.strip, sys.stdin):
        if not line:
            for chunkno in dependents:
                for i in dependents[chunkno]:
                    tree.set(i, heads[chunkno])
            for node in tree.indices:
                sys.stdout.write("\t".join(map(str,(
                    node, tree.heads[node]))) + linesep)
            sys.stdout.write(linesep)
            tree = Tree()
            i = 0
            dependents = {}
            heads = {-1:-1}
            continue
        bInfo = INFO.match(line)
        if bInfo:
            chunkno, governor, head_start, head_end = map(int, bInfo.groups())
            start = i+head_start
            end = i + head_end
            heads[chunkno] = start
            dependents.setdefault(governor, set()).add(end)
        else:
            morph, pos = line.split('\t')
            if i == end:
                tree.add(i, i) # add a dummy head for the intra head morph 
            elif i < start:
                tree.add(i, i+1) # the next word is the head
            else:
                tree.add(i, end) 
            i += 1
