from __init__ import *

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] ")
    parser.add_option("", "--prefix", dest="prefix", help="prefix", default="align")
    options, args = parser.parse_args()
    surefile = open(options.prefix+".sure", "w")
    possiblefile = open(options.prefix+".possible", "w")
    for line in map(str.strip, sys.stdin):
        lineno = line.split("|")[0]
        if not line.split("|")[1]:
            continue
        sure, possible = [], []
        for i, j, sp in map(str.split, line.split("|")[1:]):
            if sp == "s":
                sure.append("%d-%d"%(int(i)-1, int(j)-1))
                possible.append("%d-%d "%(int(i)-1, int(j)-1))
            elif sp == "p":
                possible.append("%d-%d "%(int(i)-1, int(j)-1))
        surefile.write(" ".join(sure)+linesep)
        possiblefile.write(" ".join(possible)+linesep)
    map(file.close, [surefile, possiblefile])
