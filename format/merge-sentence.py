

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    options, args = parser.parse_args()
    files = map(open, args)
    while True:
        line = [[] for j in range(len(files))]
        for i, input in enumerate(files):
            for sentence in input:
                if not sentence.strip():
                    break
                line[i].append(sentence.rstrip())
        if set(map(len, line)) == set([0]):
            break
        if len(set(map(len, line))) == 1:
            for t in zip(*line):
                print "\t".join(t)
        else:
            print "\t".join(map(" ".join, line))
