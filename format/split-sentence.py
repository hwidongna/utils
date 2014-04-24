#-*- encoding: utf-8 -*-
import sys, re
BOS = re.compile("(sdajflksjdfkl)")
EOS = re.compile("(\.|\?|\!|。|？|！)$")
PREFIX = re.compile("(Mr\.|Mrs\.|a\.m\.|p\.m\.|U\.S\.|D\.C\.|Dr\.|No\.|M\.A\.|B\.C\.|L\.A\.|J\.F\.\K\.|T\.B\.|P\.S\.|M\.S\.)")
for line in map(str.split, sys.stdin):
    bos = 0
    for i, word in enumerate(line):
        if i > bos and BOS.search(word):
            print " ".join(line[bos:i])
            bos = i
        elif EOS.search(word) and not PREFIX.match(word):
            print " ".join(line[bos:i+1])
            bos = i+1
    if bos < i:
        print " ".join(line[bos:])
    print 
