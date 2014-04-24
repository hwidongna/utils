from __init__ import *

def maxmatch(start, length, chart):
    for end in range(length+1, start+1, -1):
        if (start, end) in chart:
            return end
    return start+1

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-e", "--eojeol-table", dest="table", help="lookup table for eojeol (koma result)")
    options, args = parser.parse_args()
    
    table = {}
    for line in open(options.table):
        if not line.strip():
            continue
        eojeol, morphs = map(str.strip, line.split('\t'))
        #assert morphs not in table
        table[morphs] = eojeol
    sys.stderr.write("%d eojeols are loaded"%len(table)+linesep)

    
    for sentence in map(str.split,  sys.stdin):
        chart = {}
        for start in range(len(sentence)):
            for end in range(start+1, len(sentence)+1):
                morphs = " ".join(sentence[start:end])
                if morphs in table:
#                    chart.setdefault((start,end), set()).add( table[morphs])
                    chart[(start,end)] = table[morphs]
        start = 0
        while start < len(sentence):
            end = maxmatch(start, len(sentence), chart)
            morphs = " ".join(sentence[start:end])
            eojeol = chart.get((start,end), morphs)
            #sys.stdout.write("\t".join((str((start,end)), eojeol, morphs)))
            sys.stdout.write("\t".join((eojeol, morphs)))
            sys.stdout.write(linesep)
            start = end
        sys.stdout.write(linesep)
