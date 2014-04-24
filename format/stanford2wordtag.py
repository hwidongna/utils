import sys, re
from BeautifulSoup import BeautifulSoup
from os import linesep

if __name__=="__main__":
    input = sys.stdin
    EOC = re.compile("</corpus>")
    for line in input:
        buffer = ""
        while not EOC.match(line.strip()):
            buffer += line
            line = input.next()
        soup = BeautifulSoup(buffer)
        for sentence in soup.findAll("s"):
            if not sentence.find("word") and not sentence.find("dep"):
                for i, word in enumerate(("Sentence skipped: no PCFG fallback.").split()):
                    sys.stdout.write('\t'.join(map(lambda ustr: ustr.encode('utf8'), 
                        map(unicode,(word, word, str(i))))))
                    sys.stdout.write(linesep)
            elif not sentence.find("dep"):
                w = sentence.find("word")
                for i, word in enumerate(w.string.split()): 
                    sys.stdout.write('\t'.join(map(lambda ustr: ustr.encode('utf8'), 
                        map(unicode,(w.string, w["pos"], str(i))))))
                    sys.stdout.write(linesep)
            else:
                for w in sentence.findAll("word"):
                    assert w.string and w["pos"] and w["ind"]
                    sys.stdout.write('\t'.join(map(lambda ustr: ustr.encode('utf8'), 
                        map(unicode,(w.string, w["pos"], str(int(w["ind"])-1))))))
                    sys.stdout.write(linesep)
            sys.stdout.write(linesep)
