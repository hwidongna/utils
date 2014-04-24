import sys, re
from os import linesep, SEEK_CUR
from itertools import count

class ChartedLattice:
    def __init__(self, chartlen):
        self.chart = [{"":[0.0]} for i in range(chartlen)]
    def append(self, segment):
        i = 0
        for seg, prob in segment:
            self.chart[i].setdefault(seg, []).append(prob)
            i += len(seg)
    def toplf(self):
        node = "("
        if not options.compact:
            node += linesep
        for i in range(len(self.chart)):
            if len(self.chart[i]) == 0:
                continue
            if not options.compact:
                node += "  "
            node += "("
            if not options.compact:
                node += linesep
            norm = 0.0
            for probs in self.chart[i].values():
                norm += sum(map(float, probs))
            for seg, probs in self.chart[i].iteritems():
                if not options.compact:
                    node += "\t"
                if seg:
                    node += "('%s',%f,%d),"%(seg.encode(options.encoding), sum(map(float, probs))/norm, len(seg))
                else:
                    node += "('None',0.0,1),"
                if not options.compact:
                    node += linesep
            if not options.compact:
                node += "  "
            node += "),"
            if not options.compact:
                node += linesep
        node += ")"
        if not options.compact:
            node += linesep
        return node

BOS = re.compile("<sentence id=(\d+) k=(\d)+ logProb=.+ prob=(.+)>")
EOS = re.compile("</sentence>")
def readlines(lattice, input, limit):
    for line in input:
        if not line.strip():
            break
        metainfo = BOS.match(line.strip())
        if metainfo:
            id, k, prob = metainfo.groups()
        elif int(k) > limit:
            continue
        elif not EOS.match(line.strip()):
            segment = line.strip().decode(options.encoding).split()
            if not lattice:
                lattice = ChartedLattice(sum(map(len, segment)))
            lattice.append( [(seg, prob) for seg in segment] )
    return lattice

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] <segmentation files>...")
    parser.add_option("", "--encoding", dest="encoding", help="charater encoding", default="utf-8")
    parser.add_option("", "--compact", dest="compact", action="store_true", help="compact output in a line", default=False)
    parser.add_option("-k", "", dest="k", help="the number of difference segmentation for each segnmentation file")
    options, args = parser.parse_args()
    segfiles = map(lambda fname: open(fname, "rb"), args)
    #sys.stderr.write("merge %s"%", ".join(map(lambda f:f.name, segfiles))+linesep)
    output = sys.stdout
    i = count(0)
    while True:
        #output.write("# id=%d"%i.next()+linesep)
        lattice = None
        for input in segfiles:
            lattice = readlines(lattice, input, int(options.k))
        if not lattice:
            break
        output.write(lattice.toplf()+linesep)
    map(file.close, segfiles)
