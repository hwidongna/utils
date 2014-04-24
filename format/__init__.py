import sys, re
from os import linesep
from operator import itemgetter
from itertools import count, imap, izip
from tree import *
withlabel = lambda dline: len(dline.split("\t")) > 2
