from __init__ import *

if __name__=="__main__":
    for line in sys.stdin:
        tree = Tree()
        i = count(0)
        while line.strip():
            head = line.split()[-1]
            tree.add(i.next(), int(head)-1)
            line = sys.stdin.next()
        for t in zip(
                map(str,tree.indices),
                map(str,tree.heads),
                ):
            sys.stdout.write("\t".join(t)+linesep)
        sys.stdout.write(linesep)
