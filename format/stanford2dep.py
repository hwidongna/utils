import sys, re
from BeautifulSoup import BeautifulSoup
from os import linesep

def plain_to_dep(input):
    STANFORD = re.compile("(.+)\(.+-(\d+), .+-(\d+)\)")
    i = -1 
    for line in input:
        i += 1
        if line.strip():
            mo = STANFORD.search(line)
            relation, head, dependent = mo.groups()
            head, dependent = map(lambda x:x-1, map(int,(head, dependent)))
            if i != dependent:
                sys.stdout.write("\t".join(map(str,(i, -1, "root"))))
                sys.stdout.write(linesep)
                i += 1
            sys.stdout.write("\t".join(map(str,(dependent, head, relation))))
        else:
            i = -1
        sys.stdout.write(linesep)

def xml_to_dep(input):
    EOC = re.compile("</corpus>")
    for line in input:
        buffer = ""
        while not EOC.match(line.strip()):
            buffer += line
            line = input.next()
        soup = BeautifulSoup(buffer)
        #print soup.prettify()
        for sentence in soup.findAll("s"):
            if not sentence.find("word") and not sentence.find("dep"):
                length = -1
            elif not sentence.find("dep"):
                length = len(sentence.find("word").string.split())
            else:
                length = len(sentence.findAll("word"))
            #print "length: ", length
            triples = [(i, -1, "root") for i in range(length)]
            for dep in sentence.findAll("dep"):
                index, head = map(lambda i: int(i)-1, (dep.dependent["idx"], dep.governor["idx"]))
                triples[index] = (index, head, dep["type"])
            for t in triples:
                sys.stdout.write("\t".join(map(str,t))+linesep)
            sys.stdout.write(linesep)

if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("", "--xml", dest="is_xml_format", action="store_true", help="standord xml format",)
    options, args = parser.parse_args()
    if options.is_xml_format:
        xml_to_dep(sys.stdin)
    else:
        plain_to_dep(sys.stdin)
