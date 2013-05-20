# Name: HANYU ZHANG
# Login: CS61A-PB
# TA: RICHARD
# Section: 112
# Q1.

class Mobile(object):
    """A simple binary mobile that has branches of weights or other mobiles.

    >>> Mobile(1, 2)
    Traceback (most recent call last):
        ...
    TypeError: 1 is not a Branch
    >>> m = Mobile(Branch(1, Weight(2)), Branch(2, Weight(1)))
    >>> m.weight
    3
    >>> m.isbalanced
    True
    >>> m.left.contents = Mobile(Branch(1, Weight(1)), Branch(2, Weight(1)))
    >>> m.weight
    3
    >>> m.left.contents.isbalanced
    False
    >>> m.isbalanced # All submobiles must be balanced for m to be balanced
    False
    >>> m.left.contents.right.contents.weight = 0.5
    >>> m.left.contents.isbalanced
    True
    >>> m.isbalanced
    False
    >>> m.right.length = 1.5
    >>> m.isbalanced
    True
    """

    def __init__(self, left, right):
        "*** YOUR CODE HERE ***"
        if type(left) is not Branch:
            raise TypeError(str(left)+" is not a Branch")
        if type(right) is not Branch:
            raise TypeError(str(left)+" is not a Branch")
        self.left = left
        self.right = right

    @property
    def weight(self):
        """The total weight of the mobile."""
        "*** YOUR CODE HERE ***"
        def helper(thing):
            if type(thing) is Weight:
                return thing.weight
            elif type(thing) is Mobile:
                return helper(thing.left)+helper(thing.right)
            elif type(thing) is Branch:
                return helper(thing.contents)
        return helper(self)


    @property
    def isbalanced(self):
        """True if and only if the mobile is balanced."""
        "*** YOUR CODE HERE ***"
        if type(self) is Mobile:
            left_torque = self.left.contents.weight*self.left.length
            right_torque = self.right.contents.weight*self.right.length
            self_is_balanced = (left_torque == right_torque)
        return self.right.contents.isbalanced and self.left.contents.isbalanced and self_is_balanced

def check_positive(x):
    """Check that x is a positive number, and raise an exception otherwise.

    >>> check_positive('hello')
    Traceback (most recent call last):
    ...
    TypeError: hello is not a number
    >>> check_positive('1')
    Traceback (most recent call last):
    ...
    TypeError: 1 is not a number
    >>> check_positive(-2)
    Traceback (most recent call last):
    ...
    ValueError: -2 <= 0
    """
    "*** YOUR CODE HERE ***"
    if type(x) is int:
        if x <= 0:
            raise ValueError(str(x)+" <= 0")
    else:
        raise TypeError(str(x)+" is not a number")


class Branch(object):
    """A branch of a simple binary mobile."""

    def __init__(self, length, contents):
        if type(contents) not in (Weight, Mobile):
            raise TypeError(str(contents) + ' is not a Weight or Mobile')
        check_positive(length)
        self.length = length
        self.contents = contents

    @property
    def torque(self):
        """The torque on the branch"""
        return self.length * self.contents.weight


class Weight(object):
    """A weight."""
    def __init__(self, weight):
        check_positive(weight)
        self.weight = weight
        self.isbalanced = True


# Q2.

def interpret_mobile(s):
    """Return a Mobile described by string s by substituting one of the classes
    Branch, Weight, or Mobile for each occurrenct of the letter T.

    >>> simple = 'Mobile(T(2,T(1)), T(1,T(2)))'
    >>> interpret_mobile(simple).weight
    3
    >>> interpret_mobile(simple).isbalanced
    True
    >>> s = 'T(T(4,T(T(4,T(1)),T(1,T(4)))),T(2,T(10)))'
    >>> m = interpret_mobile(s)
    >>> m.weight
    15
    >>> m.isbalanced
    True
    """
    next_T = s.find('T')        # The index of the first 'T' in s.
    if next_T == -1:            # The string 'T' was not found in s
        try:
            return eval(s)      # Interpret s
        except TypeError as e:
            return None         # Return None if s is not a valid mobile
    for t in ('Branch', 'Weight', 'Mobile'):
        "*** YOUR CODE HERE ***"
        sub_string = s[:next_T] + t + s[(next_T + 1):]
        if type(interpret_mobile(sub_string)) is Mobile:
            return interpret_mobile(s[:next_T] + t + s[(next_T + 1):])
    return None


# Q3.

def scale_iterator(s, k):
    """Return an iterator over the elements of s scaled by a number k.

    >>> s = scale_iterator(iter(make_integer_stream(3)), 5)
    >>> next(s)
    15
    >>> next(s)
    20
    """
    "*** YOUR CODE HERE ***"
    while True:
        current = next(s) * k
        yield current
        



# Q4.

def iterator_to_stream(iterator):
    """Convert an iterator into a stream.

    >>> s = iterator_to_stream(iter([3, 2, 1]))
    >>> s.first
    3
    >>> s.rest
    Stream(2, <...>)
    >>> s.rest.rest.rest
    Rlist.empty
    """
    "*** YOUR CODE HERE ***"
    try:
        return Stream(next(iterator),lambda: iterator_to_stream(iterator))
    except StopIteration:
        return Rlist.empty


# Q5.

def scale_stream(s, k):
    """Return a stream over the elements of s scaled by a number k.

    >>> s = scale_stream(make_integer_stream(3), 5)
    >>> s.first
    15
    >>> s.rest
    Stream(20, <...>)
    >>> scale_stream(s.rest, 10)[2]
    300
    """
    return iterator_to_stream(scale_iterator(iter(s), k))


def merge(s0, s1):
    """Return a stream over the elements of increasing s0 and s1, removing
    repeats.

    >>> ints = make_integer_stream(1)
    >>> twos = scale_stream(ints, 2)
    >>> threes = scale_stream(ints, 3)
    >>> m = merge(twos, threes)
    >>> [m[i] for i in range(10)]
    [2, 3, 4, 6, 8, 9, 10, 12, 14, 15]
    """
    if s0 is Stream.empty:
        return s1
    if s1 is Stream.empty:
        return s0
    e0, e1 = s0.first, s1.first
    if e0 < e1:
        return Stream(e0, lambda: merge(s0.rest, s1))
    elif e1 < e0:
        return Stream(e1, lambda: merge(s0, s1.rest))
    else:
        "*** YOUR CODE HERE ***"
        return Stream(e1, lambda: merge(s0.rest, s1.rest))

def make_s():
    """Return a stream over all positive integers with only factors 2, 3, & 5.

    >>> s = make_s()
    >>> [s[i] for i in range(20)]
    [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36]
    """
    def rest():
        "*** YOUR CODE HERE ***"
        return merge(merge(scale_stream(s, 2), scale_stream(s, 3)), scale_stream(s, 5))
    s = Stream(1, rest)
    return s


# Q6.

class Tree:
    """An n-ary tree with internal values."""
    def __init__(self, value, branches=[]):
        self.value = value
        self.branches = branches

def values(t):
    """Yield values of a tree by interleaving iterators of the branches.

    >>> T = Tree
    >>> t = T(1, [T(2, [T(4), T(6, [T(8)])]), T(3, [T(5), T(7)])])
    >>> tuple(values(t))
    (1, 2, 3, 4, 5, 6, 7, 8)
    """
    "*** YOUR CODE HERE ***"

def interleave(*iterables):
    """Interleave elements of iterables.

    >>> tuple(interleave([1, 4], [2, 5, 7, 8], [3, 6]))
    (1, 2, 3, 4, 5, 6, 7, 8)
    """
    "*** YOUR CODE HERE ***"
    """
    http://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    from itertools import cycle, islice
    pending = len(iterables)
    nexts = cycle(iter(it).__next__ for it in iterables)
    while pending:
        try:
            for next in nexts:
                yield next()
        except StopIteration:
            pending -= 1
            nexts = cycle(islice(nexts, pending))



class Rlist(object):
    """A recursive list consisting of a first element and the rest.

    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> len(s)
    3
    >>> s[0]
    1
    >>> s[1]
    2
    >>> s[2]
    3
    """
    class EmptyList(object):
        def __repr__(self):
            return 'Rlist.empty'
        def __len__(self):
            return 0
    empty = EmptyList()

    def __init__(self, first, rest=empty):
        self.first = first
        self.rest = rest

    def __repr__(self):
        f = repr(self.first)
        if self.rest is Rlist.empty:
            return 'Rlist({0})'.format(f)
        else:
            return 'Rlist({0}, {1})'.format(f, repr(self.rest))

    def __len__(self):
        return 1 + len(self.rest)

    def __getitem__(self, k):
        if k == 0:
            return self.first
        return self.rest[k - 1]

    def __iter__(self):
        current = self
        while current is not Rlist.empty:
            yield current.first
            current = current.rest

class Stream(Rlist):
    """A lazily computed recursive list.

    >>> s = Stream(1, lambda: Stream(2+3, lambda: Stream(9)))
    >>> s.first
    1
    >>> s.rest.first
    5
    >>> s.rest
    Stream(5, <...>)
    >>> s.rest.rest.first
    9
    >>> s = Stream(1, lambda: Stream(1+2, lambda: Stream(9)))
    >>> s[2]
    9
    >>> s[0]
    1
    >>> s[1]
    3
    """
    def __init__(self, first, compute_rest=lambda: Stream.empty):
        if not callable(compute_rest):
            raise TypeError('compute_rest must be callable')
        self.first = first
        self._compute_rest = compute_rest
        self._rest = None

    @property
    def rest(self):
        """Return the rest of the stream, computing it if necessary."""
        if self._compute_rest is not None:
            self._rest = self._compute_rest()
            self._compute_rest = None
        return self._rest

    def __len__(self):
        raise NotImplementedError('length not supported on Streams')

    def __repr__(self):
        return 'Stream({0}, <...>)'.format(repr(self.first))

def make_integer_stream(first=1):
    """Return an infinite stream of increasing integers."""
    def compute_rest():
        return make_integer_stream(first+1)
    return Stream(first, compute_rest)


