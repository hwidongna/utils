from __init__ import *

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser(usage="usage: %prog files < linenum [options] ")
    parser.add_option("-i", "--inversed", dest="inversed", action="store_true", help="exclude linenum", default=False)
    options, args = parser.parse_args()

    linenum = set()
    for line in sys.stdin:
        linenum.add(int(line))

    files = map(open, args)
    def write(input):
        output = open(input.name+".filter", "w")
        for i, line in enumerate(input):
            if not options.inversed and i+1 in linenum  \
            or options.inversed and i+1 not in linenum:
                output.write(line)
        output.close()
    map(write, files)
    map(file.close, files)
