from __init__ import *

def shift(l, amount):
    return l[-amount:] + l[:-amount]

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-r", "--reverse", dest="reverse", 
            action="store_true", default=False, help="reverse direction")
    parser.add_option("-s", "--shift", dest="shift", default=0,
            help="shift column left (minus) or right (plus)")
    parser.add_option("-z", "--zero-fill", dest="zerofilled", help="zero filled column")
    parser.add_option("-i", "--inc-fill", dest="incfilled", help="incremental filled column")
    options, args = parser.parse_args()
    if options.reverse:
        while True:
            try:
                line = sys.stdin.next()
            except StopIteration:
                break
            buffer = []
            i = count(1)
            while line.strip():
                if options.zerofilled and len(line.split()) < int(options.zerofilled):
                    buffer.append(line.split()+
                            ['0']*(int(options.zerofilled)-len(line.split())))
                elif options.incfilled and len(line.split()) < int(options.incfilled):
                    buffer.append(
                            [str(i.next())]*(int(options.incfilled)-len(line.split()))+
                            line.split())
                else:
                    buffer.append(line.split())
                line = sys.stdin.next()
            for each in zip(*buffer):
                sys.stdout.write('\t'.join(shift(each,int(options.shift)))+linesep)
            sys.stdout.write(linesep)
    else:
        for line in sys.stdin:
            for word in line.split():
                sys.stdout.write(word+linesep)
            sys.stdout.write(linesep)
