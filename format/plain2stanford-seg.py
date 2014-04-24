import sys
from os import linesep

for i, line in enumerate(sys.stdin):
    sys.stdout.write("<sentence id=%d k=1 logProb=0.0 prob=1.0>"%i + linesep)
    sys.stdout.write(line)
    sys.stdout.write("</sentence>"+linesep)
