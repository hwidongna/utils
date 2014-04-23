from __init__ import *

def setweight(variables):
    #assert all(map(lambda w: 0.0 <= float(w) <= 1.0, options.weight))
    if options.unweighted:
        normalized = [1.0] * len(variables) 
    elif options.weight != None:
        assert options.ishead, "conficting weight strategies. choose either --head-weight or --weight"
        denom = sum(map(float,options.weight.split()))
        assert denom != 0
        normalized = map(lambda x: x/denom, map(float, options.weight.split()))
        #assert sum(normalized) == 1.0, sum(normalized)
        assert len(variables) == len(normalized), "incorrect weight vector (length should be %d)"%len(variables)
    elif options.ishead:
        normalized = map(itemgetter(0), variables)
    else:
        normalized = [1.0 / len(variables) ]*len(variables)
    #sys.stderr.write("normalized weight vector: %s"%", ".join(map(str, normalized))+linesep)
    return normalized

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog [options] < 2-dimensional table > summed")
    parser.add_option("-i", "--incremental", dest="incremental", action="store_true", help="do not store 2-dimensional data", default=False)
    parser.add_option("", "--head-weight", dest="ishead", action="store_true", help="use head col for weight", default=False)
    parser.add_option("-u", "--unweighted", dest="unweighted", action="store_true", help="unweighted sum (accumulation)", default=False)
    parser.add_option("-r", "--row-sum", dest="rowsum", action="store_true", help="sum of row direction", default=False)
    parser.add_option("-w", "--weight", dest="weight", help="weighted sum (to be normalized)")
    options, args = parser.parse_args()
    assert not (options.ishead and options.rowsum), "do not support head row weight yet"
    if options.weight != None:
        sys.stderr.write("original weight vector: %s"%", ".join(options.weight.split())+linesep)

    weighted_sum = lambda l,w: sum(a*b for a, b in zip(l,w))
    if options.rowsum:
        for line in sys.stdin:
            if not line.strip():
                sys.stdout.write(linesep)
                continue
            variables = map(float, line.split())
            normalized = setweight(variables)
            sys.stdout.write(str(weighted_sum(variables, normalized)) + linesep)
    elif options.incremental:
        assert options.ishead
        for line in sys.stdin:
            variables = []
            while line.strip():
                if not variables:
                    variables = [0.0] * (len(line.split())-1)
                var = map(float, line.split())
                weight, var = var[0], var[1:]
                variables = map(lambda a,b:a+b, variables, map(lambda x: weight*x, var))
                try:
                    line = sys.stdin.next()
                except StopIteration:
                    break
            if not variables:
                sys.stdout.write(linesep)
                continue
            sys.stdout.write("\t".join(map(str, variables)) + linesep)
    else:
        for line in sys.stdin:
            variables = []
            while line.strip():
                variables.append(map(float, line.split()))
                try:
                    line = sys.stdin.next()
                except StopIteration:
                    break
            if not variables:
                sys.stdout.write(linesep)
                continue
            normalized = setweight(variables)
            if options.ishead:
                variables = map(lambda v: v[1:], variables)
            sys.stdout.write("\t".join(map(str, map(lambda l: weighted_sum(l, normalized), zip(*variables)))) + linesep)
