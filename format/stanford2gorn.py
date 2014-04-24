import sys, re
from BeautifulSoup import BeautifulSoup
from __init__ import *

PRETERMINAL = re.compile("\(([^\(\)]+) [^\(\)]+\)")
NONTERMINAL = re.compile("\(([^\(\)]+)")

class GornAddress:
    def __init__(self):
        self.address = [0]
    def __str__(self):
        return ".".join(map(str,self.address))
    def __repr__(self):
        return str(self)
    def next(self):
        if self.address:
            self.address = self.address[:-1] + [self.address[-1]+1]
    def inc(self):
        self.address.append(1)
    def dec(self, level):
        self.address = self.address[:level+1] 
    def depth(self):
        return len(self.address)-1

if __name__=="__main__":
    input = sys.stdin
    EOC = re.compile("</corpus>")
    for line in input:
        buffer = ""
        while not EOC.match(line.strip()):
            buffer += line
            line = input.next()
        soup = BeautifulSoup(buffer)
        for sentence in soup.findAll("s"):
            i = count(0)
            tree = sentence.find("tree", style="penn")
            depth = 0 
            gorn = GornAddress()
            for node in filter(str.strip, map(str, tree.contents[0].splitlines())):
                nonterminal = NONTERMINAL.search(node)
                assert nonterminal
                if not PRETERMINAL.match(node.lstrip()):
                    sys.stdout.write("\t".join(map(str.strip,map(str, 
                        (-1, nonterminal.group(1), gorn.depth(), gorn))))+linesep)
                    gorn.inc()
                preterminals = PRETERMINAL.search(node)
                while preterminals:
                    sys.stdout.write("\t".join(map(str.strip, map(str,
                        (i.next(), preterminals.group(1), gorn.depth(), gorn))))+linesep)
                    preterminals = PRETERMINAL.search(node, preterminals.start()+1)
                    if preterminals:
                        gorn.next()
                depth += node.count("(") - node.count(")")
                gorn.dec(depth)
                if node.count(")") > 0:
                    gorn.next()
            sys.stdout.write(linesep)
