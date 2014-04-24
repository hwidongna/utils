from operator import itemgetter
from itertools import chain, combinations

class Tree:
    is_root = lambda self, node: node in self.dependents.get(-1,[])
    is_head = lambda self, node: node in self.dependents
    roots = lambda self: self.dependents.get(-1,[])
    i_order = lambda self: tuple(enumerate(self.offsets))
    def __init__(self):
        self.indices = []
        self.heads = [] # zero-based index 
        self.offsets = [] # relative order to head and siblings
        self.dependents = {} # zero-based index 
    def __iter__(self):
        for root in self.roots():
            for index in self.inorder(root, self.i_order()):
                yield index
    def __str__(self):
        return joined_str(self.indices, iter(self))
    def __len__(self):
        assert len(self.indices)==len(self.heads)==len(self.offsets)
        return len(self.indices)
    def __getitem__(self, i):
        return self.indices[i]
    def add(self, index, head):
        index, head = map(int,(index, head))
        self.indices.append(index)
        self.heads.append(head)
        self.offsets.append(len(self.indices)-1-head)
        if index != head:
            self.dependents.setdefault(head, []).append(len(self.indices)-1)
    def set(self, index, head):
        self.heads[self.index(index)] = head
        assert index != head
        self.dependents.setdefault(head, []).append(self.index(index))
    def inorder(self, head, i_order):
        target = self.dependents.get(head,[])
        target_i_order = map(lambda i: i_order[i], target) + [(head, 0)]
        for i, order in sorted(target_i_order, key=itemgetter(1,0)):
            if i == head:
                yield head
                continue
            for index in self.inorder(i, i_order):
                yield index
    def preorder(self, head, i_order):
        yield head
        target = self.dependents.get(head,[])
        target_i_order = map(lambda i: i_order[i], target)
        for i, order in sorted(target_i_order, key=itemgetter(1,0)):
            for index in self.preorder(i, i_order):
                yield index
    def postorder(self, head, i_order):
        target = self.dependents.get(head,[])
        target_i_order = map(lambda i: i_order[i], target)
        for i, order in sorted(target_i_order, key=itemgetter(1,0)):
            for index in self.postorder(i, i_order):
                yield index
        yield head
    def index(self, node):
        return self.indices.index(node)
    def ancestors(self, node):
        result = []
        while not self.is_root(node):
            result.append(self.heads[node])
            node = self.heads[node]
        return result
    def descendants(self, node):
        result = set()
        if not node in self.dependents:
            return result
        result.update(self.dependents[node])
        for d in self.dependents[node]:
            result.update(self.descendants(d))
        return result
    def leaves(self, node):
        if not node in self.dependents:
            yield node
        for dep in self.dependents.get(node, []):
            for leaf in self.leaves(dep):
                yield leaf
    def rootof(self, nodeseq):
        for node in nodeseq:
            if not self.heads[node] in nodeseq:
                yield node
    def headof(self, nodeseq):
        for node in nodeseq:
            if not self.heads[node] in nodeseq:
                yield self.heads[node]
    def is_treelet(self, nodeseq):
        return len(tuple(self.rootof(nodeseq))) == 1
    def treelet(self, head, maxlen):
        if maxlen <= 0:
            return
        yield (head,)
        for treelet in powerset(tuple(flatten(
                self.treelet(node, maxlen-1) for node in self.dependents.get(head, [])))):
            if len(treelet) == 0:
                continue
            elif len(treelet) > maxlen-1:
                break
            yield (head,) + treelet
    def treeseq(self, treeletlist, maxlen):
        if not treeletlist:
            return
        for i in range(len(treeletlist)):
            for treelet in treeletlist[i]:
                yield treelet
                for seq in self.treeseq(treeletlist[i+1:], maxlen):
                    if len(treelet + seq) > maxlen:
                        break
                    yield treelet + seq
    def wellformed(self, nodeseq):
        return len(set(self.headof(nodeseq))) == 1

    def readline(stream):
        tree = Tree()
        for line in stream:
            if not line.strip():
                break
            index, head = map(int, line.split()[:2])
            tree.add(index, head)
        return tree
    readline = staticmethod(readline)

def joined_str(seq, indices, joiner=" "):
    return joiner.join(map(lambda i:str(seq[i]), indices))

def intsplit(seq, start=None, end=None):
    if start and end:
        return map(int,str.split(seq)[start:end])
    elif start:
        return map(int,str.split(seq)[start:])
    elif end:
        return map(int,str.split(seq)[:end])
    return map(int,str.split(seq))

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def flatten(seq, verbose=False):
    if verbose:
        yield "("
    for x in seq:
        if not hasattr(x, '__iter__') or not flatten(x, verbose):
            yield x
        else:
            for y in flatten(x, verbose):
                yield y
    if verbose:
        yield ")"

import unittest
class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.g = None
    def tearDown(self):
        try:
            if self.g:
                while True:
                    try:
                        next = self.g.next()
                        print "remaining element", next
                    except StopIteration:
                        break
        except:
            print self.g

class TestSimpleTree(TestGenerator):
    def setUp(self):
        TestGenerator.setUp(self)
        self.tree = Tree()
        self.tree.add(0, head=-1)
        self.tree.add(1, head=0)
    def test_add(self):
        self.assertEquals({0:[1], -1:[0]}, self.tree.dependents)
        self.assertEquals([0,1], list(iter(self.tree)))
        self.tree.add("2", head=0)
        self.assertEquals({0:[1,2], -1:[0]}, self.tree.dependents)
    def test_treelet_leaf(self):
        self.g = self.tree.treelet(head=1, maxlen=len(self.tree))
        self.assertEquals((1,), self.g.next())
    def test_treelet_root(self):
        self.g = self.tree.treelet(head=0, maxlen=len(self.tree))
        self.assertEquals((0,), self.g.next())
        self.assertEquals((0,1,), self.g.next())
    def test_treelet_root_limit(self):
        self.g = self.tree.treelet(head=0, maxlen=1)
        self.assertEquals((0,), self.g.next())
    def test_treeseq0(self):
        treeletset = {0:set([(0,)])}
        self.g = self.tree.treeseq(map(itemgetter(1), sorted(treeletset.iteritems())), maxlen=1)
        self.assertEquals((0,), self.g.next())
    def test_treeseq(self):
        treeletset = {0:set([(0,), (0,1,)])}
        self.g = self.tree.treeseq(map(itemgetter(1), sorted(treeletset.iteritems())), maxlen=2)
        self.assertEquals((0,1,), self.g.next())
        self.assertEquals((0,), self.g.next())
    def test_treeseq2(self):
        treeletset = {0:set([(0,)]), 1:set([(1,), (1,2)])}
        self.g = self.tree.treeseq(map(itemgetter(1), sorted(treeletset.iteritems())), maxlen=3)
        self.assertEquals((0,), self.g.next())
        self.assertEquals((0,1,2,), self.g.next())
        self.assertEquals((0,1,), self.g.next())
        self.assertEquals((1,2,), self.g.next())
        self.assertEquals((1,), self.g.next())
    def test_treeseq3(self):
        treeletset = {0:set([(0,)]), 1:set([(1,)]), 2:set([(2,)])}
        self.g = self.tree.treeseq(map(itemgetter(1), sorted(treeletset.iteritems())), maxlen=3)
        self.assertEquals((0,), self.g.next())
        self.assertEquals((0,1,), self.g.next())
        self.assertEquals((0,1,2,), self.g.next())
        self.assertEquals((0,2,), self.g.next())
        self.assertEquals((1,), self.g.next())
        self.assertEquals((1,2,), self.g.next())
        self.assertEquals((2,), self.g.next())
    def test_leaves(self):
        self.g = self.tree.leaves(0)
        self.assertEquals(1, self.g.next())
    def test_leaves_leaf(self):
        self.g = self.tree.leaves(1)
        self.assertEquals(1, self.g.next())
    def test_real(self):
        self.tree = Tree()
        self.tree.add(0, head=10)
        self.tree.add(1, head=2)
        self.tree.add(2, head=3)
        self.tree.add(3, head=4)
        self.tree.add(4, head=5)
        self.tree.add(5, head=6)
        self.tree.add(6, head=8)
        self.tree.add(7, head=8)
        self.tree.add(8, head=10)
        self.tree.add(9, head=10)
        self.tree.add(10, head=-1)
        self.assertEquals(list(range(11)), list(iter(self.tree)))
        self.tree.offsets = (-3,-1,-1,-1,-1,-1,-2,-1,-2,-1,0)
        self.assertEquals(list(range(11)), list(iter(self.tree)))

class TestMultiLevelTree(TestGenerator):
    def setUp(self):
        TestGenerator.setUp(self)
        self.tree = Tree()
        self.tree.add(0, head=-1)
        self.tree.add(1, head=0)
        self.tree.add(2, head=1)
    def test_add(self):
        self.assertEquals([0,1,2], list(iter(self.tree)))
        self.assertEquals({0:[1], 1:[2], -1:[0]}, self.tree.dependents)
    def test_iter(self):
        self.assertEquals([0,1,2], list(iter(self.tree)))
        self.tree.offsets = [0,-1,-1]
        self.assertEquals([2,1,0], list(iter(self.tree)))

        self.tree = Tree()
        self.tree.add(2, head=1)
        self.tree.add(1, head=2)
        self.tree.add(0, head=-1)
        self.assertEquals([0,1,2], list(iter(self.tree)))
        self.tree.offsets = [-1,-1,0]
        self.assertEquals([0,1,2], list(iter(self.tree)))
        self.tree.offsets = [1,1,0]
        self.assertEquals([2,1,0], list(iter(self.tree)))
        self.assertEquals([0,1,2], map(lambda i:self.tree.indices[i], list(iter(self.tree))))
    def test_leaves(self):
        self.g = self.tree.leaves(0)
        self.assertEquals(2, self.g.next())

class TestMiddleHead(TestGenerator):
    def setUp(self):
        TestGenerator.setUp(self)
        self.tree = Tree()
        self.tree.add(0, head=2)
        self.tree.add(1, head=2)
        self.tree.add(2, head=-1)
        self.tree.add(3, head=2)
        self.tree.add(4, head=2)
    def test(self):
        self.assertEquals([0,1,2,3,4], list(iter(self.tree)))
    def test_leaves(self):
        self.g = self.tree.leaves(2)
        self.assertEquals(0, self.g.next())
        self.assertEquals(1, self.g.next())
        self.assertEquals(3, self.g.next())
        self.assertEquals(4, self.g.next())
    def test_rootof(self):
        f0, = self.tree.rootof([0])
        self.assertEquals(0, f0)
        f1_f2, = self.tree.rootof([1,2])
        self.assertEquals(2, f1_f2)
        f1_f2_f3, = self.tree.rootof([1,2,3])
        self.assertEquals(2, f1_f2_f3)
        f3, f4, = self.tree.rootof([3,4])
        self.assertEquals(3, f3)
        self.assertEquals(4, f4)
    def test_treelet_leaf(self):
        self.g = self.tree.treelet(head=1, maxlen=len(self.tree))
        self.assertEquals((1,), self.g.next())
    def test_treelet_root(self):
        self.g = self.tree.treelet(head=2, maxlen=len(self.tree))
        self.assertEquals((2,), self.g.next())
        self.assertEquals((2,0,), self.g.next())
        self.assertEquals((2,1,), self.g.next())
        self.assertEquals((2,3,), self.g.next())
        self.assertEquals((2,4,), self.g.next())
        self.assertEquals((2,0,1), self.g.next())
        self.assertEquals((2,0,3), self.g.next())
        self.assertEquals((2,0,4), self.g.next())
        self.assertEquals((2,1,3), self.g.next())
        self.assertEquals((2,1,4), self.g.next())
        self.assertEquals((2,3,4), self.g.next())
        self.assertEquals((2,0,1,3), self.g.next())
        self.assertEquals((2,0,1,4), self.g.next())
        self.assertEquals((2,0,3,4), self.g.next())
        self.assertEquals((2,1,3,4), self.g.next())
        self.assertEquals((2,0,1,3,4), self.g.next())
    def test_treelet_root_limit(self):
        self.g = self.tree.treelet(head=2, maxlen=2)
        self.assertEquals((2,), self.g.next())
        self.assertEquals((2,0,), self.g.next())
        self.assertEquals((2,1,), self.g.next())
        self.assertEquals((2,3,), self.g.next())
        self.assertEquals((2,4,), self.g.next())

if __name__=="__main__":
    unittest.main()
