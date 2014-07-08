# -*- encoding: utf-8 -*-
import os, sys, re
from itertools import izip, imap

korean = open(sys.argv[1])
english = open(sys.argv[2])
kout = open(sys.argv[1]+".clean", "w")
eout = open(sys.argv[2]+".clean", "w")

minlen = int(sys.argv[3])
maxlen = int(sys.argv[4])

A = u'\u0041'
Z = u'\u005A'
a = u'\u0061'
z = u'\u007A'
HREF = re.compile("\[ http://.*\]")

def has_latin(uline):
    for ch in uline:
        if A <= ch <= Z or a <= ch <= z:
            return True
    return False

HANJA_START = u'\u4E00'
HANJA_END = u'\u9FFF'

def has_hanja(uline):
    for ch in uline:
        if HANJA_START <= ch <= HANJA_END:
            print ch.encode("utf-8")
            return True
    return False

def remove_href(line):
    return HREF.sub("", line)

while True:
    try:
        lines = map(file.next, [korean, english])
    except StopIteration:
        break
    kline, eline = map(remove_href, lines)
    uline = kline.decode("utf-8")
    klen = len(kline.split())
    elen = len(eline.split())
    if not has_hanja(uline) \
    and minlen <= klen <= maxlen and minlen <= elen <= maxlen:
    #and kline.rstrip().endswith(".") and eline.rstrip().endswith("."):
        kout.write(kline)
        eout.write(eline)

map(file.close, [korean, english, kout, eout])
