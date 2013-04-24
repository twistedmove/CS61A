# Name: Hanyu Zhang
# Login: cs61a-pf
# TA: Richard
# Section: 112

def empty(s):
    return len(s) == 0

def set_contains2(s, v):
    """Return true if set s contains value v as an element.

    >>> set_contains2(s, 2)
    True
    >>> set_contains2(s, 5)
    False
    """
    if empty(s) or s.first > v:
        return False
    if s.first == v:
        return True
    return set_contains2(s.rest, v)

def intersect_set2(set1, set2):
    """Return a set containing all elements common to set1 and set2.

    >>> t = Rlist(2, Rlist(3, Rlist(4)))
    >>> intersect_set2(s, t)
    Rlist(2, Rlist(3))
    """
    if empty(set1) or empty(set2):
        return Rlist.empty
    e1, e2 = set1.first, set2.first
    if e1 == e2:
        return Rlist(e1, intersect_set2(set1.rest, set2.rest))
    if e1 < e2:
        return intersect_set2(set1.rest, set2)
    if e2 < e1:
        return intersect_set2(set1, set2.rest)

# Q1.

def adjoin_set2(s, v):
    """Return a set containing all elements of s and element v.

    >>> adjoin_set2(s, 2.5)
    Rlist(1, Rlist(2, Rlist(2.5, Rlist(3))))
    """
    "*** YOUR CODE HERE ***"
    if empty(s):
        return Rlist(v)  
    if v < s.first:
        return Rlist(v, s)
    if v == s.first:
        return s
    if v > s.first:
        return Rlist(s.first, adjoin_set2(s.rest, v))


# Q2.

def union_set2(set1, set2):
    """Return a set containing all elements either in set1 or set2.

    >>> t = Rlist(1, Rlist(3, Rlist(5)))
    >>> union_set2(s, t)
    Rlist(1, Rlist(2, Rlist(3, Rlist(5))))
    """
    "*** YOUR CODE HERE ***"
    for i in range(0, len(set1)):
        set2=adjoin_set2(set2, set1[i])
    return set2


def set_contains3(s, v):
    """Return true if set s contains value v as an element.

    >>> t = Tree(2, Tree(1), Tree(3))
    >>> set_contains3(t, 3)
    True
    >>> set_contains3(t, 0)
    False
    >>> set_contains3(big_tree(20, 60), 34)
    True
    """
    if s is None:
        return False
    if s.entry == v:
        return True
    if s.entry < v:
        return set_contains3(s.right, v)
    if s.entry > v:
        return set_contains3(s.left, v)

def adjoin_set3(s, v):
    """Return a set containing all elements of s and element v.

    >>> b = big_tree(0, 9)
    >>> b
    Tree(4, Tree(1), Tree(7, None, Tree(9)))
    >>> adjoin_set3(b, 5)
    Tree(4, Tree(1), Tree(7, Tree(5), Tree(9)))
    """
    if s is None:
        return Tree(v)
    if s.entry == v:
        return s
    if s.entry < v:
        return Tree(s.entry, s.left, adjoin_set3(s.right, v))
    if s.entry > v:
        return Tree(s.entry, adjoin_set3(s.left, v), s.right)

# Q3.

def depth(s, v):
    """Return the depth of the value v in tree set s.

    The depth of a value is the number of branches followed to reach the value.
    The depth of the root of a tree is always 0.

    >>> b = big_tree(0, 9)
    >>> depth(b, 4)
    0
    >>> depth(b, 7)
    1
    >>> depth(b, 9)
    2
    """
    "*** YOUR CODE HERE ***"
    assert set_contains3(s, v), "v is not in s"
    def helper(s, v, depth):
        if s.entry == v:
            return depth
        if s.entry < v:
            return helper(s.right, v, depth + 1)
        if s.entry > v:
          return set_contains3(s.left, v, depth + 1)
    return helper(s, v, 0)    

# Q4.

def tree_to_ordered_sequence(s):
    """Return an ordered sequence containing the elements of tree set s.

    >>> b = big_tree(0, 9)
    >>> tree_to_ordered_sequence(b)
    Rlist(1, Rlist(4, Rlist(7, Rlist(9))))
    """
    "*** YOUR CODE HERE ***"
    if s is None: return Rlist.empty
    a = Rlist(s.entry)
    l = []
    def helper(s):
        if s is not None:
            l.append(s.entry)
            helper(s.left)
            helper(s.right)            
    helper(s)
    for i in l:
        a = adjoin_set2(a, i)
    return a        

    


# Q5.

def partial_tree(s, n):
    """Return a balanced tree of the first n elements of Rlist s, along with
    the rest of s. A tree is balanced if the length of the path to any two
    leaves are at most one apart.

    >>> s = Rlist(1, Rlist(2, Rlist(3, Rlist(4, Rlist(5)))))
    >>> partial_tree(s, 3)
    (Tree(2, Tree(1), Tree(3)), Rlist(4, Rlist(5)))
    """
    if n == 0:
        return None, s
    "*** YOUR CODE HERE ***"
    tail_s = s
    for _ in range(0, n): tail_s = tail_s.rest
    if tail_s is Rlist.empty: tail_s = None
    head_s = [s[i] for i in range(0, n)]
    left_size = (n-1)//2
    def helper(left_s):
        n = len(left_s)
        if n == 0: return None    
        left_size = (n-1)//2
        return Tree(left_s[left_size],
                    helper(left_s[:left_size]), 
                    helper(left_s[left_size + 1:]) )
    return Tree(head_s[left_size],helper(head_s[:left_size]), helper(head_s[left_size+1 :])), tail_s

    

def ordered_sequence_to_tree(s):
    """Return a balanced tree containing the elements of ordered Rlist s.

    A tree is balanced if the lengths of the paths from the root to any two
    leaves are at most one apart.

    Note: this implementation is complete, but the definition of partial_tree
    below is not complete.

    >>> ordered_sequence_to_tree(Rlist(1, Rlist(2, Rlist(3))))
    Tree(2, Tree(1), Tree(3))
    >>> b = big_tree(0, 20)
    >>> elements = tree_to_ordered_sequence(b)
    >>> elements
    Rlist(1, Rlist(4, Rlist(7, Rlist(10, Rlist(13, Rlist(16, Rlist(19)))))))
    >>> ordered_sequence_to_tree(elements)
    Tree(10, Tree(4, Tree(1), Tree(7)), Tree(16, Tree(13), Tree(19)))
    """
    return partial_tree(s, len(s))[0]


def intersect_set3(set1, set2):
    """Return a set containing all elements common to set1 and set2.


    >>> s, t = big_tree(0, 12), big_tree(6, 18)
    >>> intersect_set3(s, t)
    Tree(8, Tree(6), Tree(10, None, Tree(12)))
    """
    s1, s2 = map(tree_to_ordered_sequence, (set1, set2))
    return ordered_sequence_to_tree(intersect_set2(s1, s2))

def union_set3(set1, set2):
    """Return a set containing all elements either in set1 or set2.

    >>> s, t = big_tree(6, 12), big_tree(10, 16)
    >>> union_set3(s, t)
    Tree(10, Tree(6, None, Tree(9)), Tree(13, Tree(11), Tree(15)))
    """
    s1, s2 = map(tree_to_ordered_sequence, (set1, set2))
    return ordered_sequence_to_tree(union_set2(s1, s2))


class Rlist(object):
    """A recursive list consisting of a first element and the rest."""

    class EmptyList(object):
        def __len__(self):
            return 0

    empty = EmptyList()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        args = repr(self.first)
        if self.rest is not Rlist.empty:
            args += ', {0}'.format(repr(self.rest))
        return 'Rlist({0})'.format(args)

    def __len__(self):
        return 1 + len(self.rest)

    def __getitem__(self, i):
        if i == 0:
            return self.first
        return self.rest[i-1]

def extend_rlist(s1, s2):
    """Return a list containing the elements of s1 followed by those of s2."""
    if s1 is Rlist.empty:
        return s2
    return Rlist(s1.first, extend_rlist(s1.rest, s2))

def map_rlist(s, fn):
    """Return a list resulting from mapping fn over the elements of s."""
    if s is Rlist.empty:
        return s
    return Rlist(fn(s.first), map_rlist(s.rest, fn))

def filter_rlist(s, fn):
    """Filter the elemenst of s by predicate fn."""
    if s is Rlist.empty:
        return s
    rest = filter_rlist(s.rest, fn)
    if fn(s.first):
        return Rlist(s.first, rest)
    return rest

s = Rlist(1, Rlist(2, Rlist(3))) # A set is an Rlist with no duplicates

class Tree(object):
    """A tree with internal values."""

    def __init__(self, entry, left=None, right=None):
        self.entry = entry
        self.left = left
        self.right = right

    def __repr__(self):
        args = repr(self.entry)
        if self.left or self.right:
            args += ', {0}, {1}'.format(repr(self.left), repr(self.right))
        return 'Tree({0})'.format(args)

def big_tree(left, right):
    """Return a tree of elements between left and right.

    >>> big_tree(0, 12)
    Tree(6, Tree(2, Tree(0), Tree(4)), Tree(10, Tree(8), Tree(12)))
    """
    if left > right:
        return None
    split = left + (right - left)//2
    return Tree(split, big_tree(left, split-2), big_tree(split+2, right))


