# Name: Hanyu Zhang
# Login: cs61a-pb
# TA: Richard
# Section: 112
# Q1.

from fractions import gcd

class Rational(object):
    """A mutable fraction.

    >>> f = Rational(3, 5)
    >>> f
    Rational(3, 5)
    >>> print(f)
    3/5
    >>> f.float_value
    0.6
    >>> f.numerator = 4
    >>> f.float_value
    0.8
    >>> f.denominator -= 3
    >>> f.float_value
    2.0
    """

    def __init__(self, numer, denom):
        g = gcd(numer, denom)
        self.numerator = numer // g
        self.denominator = denom // g

    @property
    def float_value(self):
        return self.numerator / self.denominator

    def __repr__(self):
        return 'Rational({0}, {1})'.format(self.numerator,
                                           self.denominator)

    def __str__(self):
        return '{0}/{1}'.format(self.numerator, self.denominator)

    def __add__(self, num):
        return add_rational(self, num)

    def __mul__(self, num):
        return mul_rational(self, num)

    def __eq__(self, num):
        return eq_rational(self, num)

    def __bool__(self):
        return self.numerator != 0

def add_rational(r1, r2):
    denom = r1.denominator * r2.denominator
    numer1 = r1.numerator * r2.denominator
    numer2 = r1.denominator * r2.numerator
    return Rational(numer1 + numer2, denom)

def mul_rational(r1, r2):
    return Rational(r1.numerator * r2.numerator,
                    r1.denominator * r2.denominator)

def eq_rational(r1, r2):
        return (r1.numerator * r2.denominator ==
                r2.numerator * r1.denominator)


class ImmutableRational(Rational):
    """An immutable fraction.

    >>> f = ImmutableRational(3, 5)
    >>> f
    ImmutableRational(3, 5)
    >>> f.numerator = 4
    >>> f
    ImmutableRational(3, 5)
    >>> f.denominator -= 3
    >>> f
    ImmutableRational(3, 5)
    """

    def __init__(self, numer, denom):
        Rational.__init__(self, numer, denom)
        self.finalized = True

    def __setattr__(self, attr, value):
        if hasattr(self, 'finalized') and self.finalized:
            return
        object.__setattr__(self, attr, value)

    def __repr__(self):
        return 'ImmutableRational({0}, {1})'.format(self.numerator,
                                                    self.denominator)


def mutate_rational(r):
    """Mutate a rational by adding one to its denominator.

    >>> f = ImmutableRational(3, 5)
    >>> f
    ImmutableRational(3, 5)
    >>> mutate_rational(f)
    >>> f
    ImmutableRational(3, 6)
    """
    "*** YOUR CODE HERE ***"
    Rational.__setattr__(r, 'denominator', r.denominator + 1)

# Q2.

class Amount(object):
    """An amount of nickels and pennies.

    >>> a = Amount(3, 7)
    >>> a.nickels
    3
    >>> a.pennies
    7
    >>> a.value
    22
    >>> a.nickels = 5
    >>> a.value
    32
    """
    "*** YOUR CODE HERE ***"
    def __init__(self, nickels, pennies):
        self.nickels = nickels
        self.pennies = pennies
    @property
    def value(self):
        return self.nickels * 5 + self.pennies
    @value.setter
    def value(self, amount):
        self.value = amount

class MinimalAmount(Amount):
    """An amount of nickels and pennies that is initialized with no more than
    four pennies, by converting excess pennies to nickels.

    >>> a = MinimalAmount(3, 7)
    >>> a.nickels
    4
    >>> a.pennies
    2
    >>> a.value
    22
    """
    "*** YOUR CODE HERE ***"
    def __init__(self, nickels, pennies):
        if pennies > 4:
            nickels += pennies // 5
            pennies -= 5 * (pennies // 5)
        Amount.__init__(self, nickels, pennies)

# Q3.

class Square(object):
    def __init__(self, side):
        self.side = side

class Rect(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

def type_tag(s):
    return type_tag.tags[type(s)]

type_tag.tags = {Square: 's', Rect: 'r'}

def apply(operator_name, shape):
    """Apply operator to shape.

    >>> apply('area', Square(10))
    100
    >>> apply('perimeter', Square(5))
    20
    >>> apply('area', Rect(5, 10))
    50
    >>> apply('perimeter', Rect(2, 4))
    12
    """
    "*** YOUR CODE HERE ***"
    def area_rectangle(rectangle):
        return rectangle.width * rectangle.height
    def perimeter_rectangle(rectangle):
        return (rectangle.height + rectangle.width) * 2
    def area_square(square):
        return square.side ** 2
    def perimeter_square(square):
        return 4 * square.side
    implementations = { ('area', 'r'): area_rectangle,
                        ('perimeter', 'r'): perimeter_rectangle,
                        ('area', 's'): area_square,
                        ('perimeter', 's'): perimeter_square }
    return implementations[operator_name, type_tag(shape)](shape)

# Q4.

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

    def __getitem__(self, i):
        if i == 0:
            return self.first
        return self.rest[i - 1]

def map_rlist(fn, s):
    """Return an Rlist resulting from mapping fn over the elements of s.

    >>> s = Rlist(1, Rlist(2, Rlist(3)))
    >>> map_rlist(lambda x: x * x, s)
    Rlist(1, Rlist(4, Rlist(9)))
    """
    if s is Rlist.empty:
        return s
    return Rlist(fn(s.first), map_rlist(fn, s.rest))


def deep_map_rlist(fn, s):
    """Return an Rlist with the same structure as s but with fn mapped over
    its elements. An element that is an Rlist will have fn recursively mapped
    over its elements.

    >>> s = Rlist(1, Rlist(Rlist(2, Rlist(3)), Rlist(4)))
    >>> deep_map_rlist(lambda x: x * x, s)
    Rlist(1, Rlist(Rlist(4, Rlist(9)), Rlist(16)))
    """
    "*** YOUR CODE HERE ***"
    if s is Rlist.empty:
        return s
    if type(s) is not Rlist:
        return fn(s)
    return Rlist(deep_map_rlist(fn,s.first), deep_map_rlist(fn, s.rest))

# Q5.

def has_cycle(s):
    """Return whether Rlist s contains a cycle.

    >>> s = Rlist(1, Rlist(2, Rlist(3, Rlist(4, Rlist(5)))))
    >>> s.rest.rest.rest.rest.rest = s.rest.rest
    >>> has_cycle(s)
    True
    >>> t = Rlist(1, Rlist(2, Rlist(3, Rlist(4, Rlist(5)))))
    >>> has_cycle(t)
    False
    """
    "*** YOUR CODE HERE ***"
    copy = s
    list_of_rlist = []
    while copy is not Rlist.empty:
        if copy not in list_of_rlist:
            list_of_rlist.append(copy)
        else: return True
        copy = copy.rest
    return False


def has_cycle_constant(s):
    """Return whether Rlist s contains a cycle.

    >>> s = Rlist(1, Rlist(2, Rlist(3, Rlist(4, Rlist(5)))))
    >>> s.rest.rest.rest = s
    >>> has_cycle_constant(s)
    True
    >>> t = Rlist(1, Rlist(2, Rlist(3, Rlist(4, Rlist(5)))))
    >>> has_cycle_constant(t)
    False
    """
    "*** YOUR CODE HERE ***"
    copy = s
    r, t = copy, copy.rest
    while r is not Rlist.empty and t is not Rlist.empty:
        if r == t: return True
        else: 
            r, t= r.rest, t.rest.rest
    return False



