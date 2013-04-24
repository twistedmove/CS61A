# Name: Hanyu Zhang
# Login: cs61a-pb
# TA: Richard
# Section: 112
# Q1.

empty_rlist = None

def rlist(first, rest):
    """Construct a recursive list from its first element and the
    rest."""
    return (first, rest)

def first(s):
    """Return the first element of a recursive list s."""
    return s[0]

def rest(s):
    """Return the rest of the elements of a recursive list s."""
    return s[1]


def reverse_rlist_iterative(s):
    """Return a reversed version of a recursive list s.

    >>> primes = rlist(2, rlist(3, rlist(5, rlist(7, empty_rlist))))
    >>> reverse_rlist_iterative(primes)
    (7, (5, (3, (2, None))))
    """
    "*** YOUR CODE HERE ***"
    newlist = rlist(first(s), empty_rlist)
    while rest(s) != empty_rlist:
        s = rest(s)
        newlist = rlist(first(s), newlist)
    return newlist

def reverse_rlist_recursive(s):
    """Return a reversed version of a recursive list s.

    >>> primes = rlist(2, rlist(3, rlist(5, rlist(7, empty_rlist))))
    >>> reverse_rlist_recursive(primes)
    (7, (5, (3, (2, None))))
    """
    "*** YOUR CODE HERE ***"
    def helper(s, newlist):
        if rest(s) == empty_rlist:
            newlist = rlist(first(s), newlist)
            return newlist
        else: 
            newlist = rlist(first(s), newlist)
            return helper(rest(s), newlist)

    return helper(s, empty_rlist)


# Q2.

def interleave_recursive(s0, s1):
    """Interleave recursive lists s0 and s1 to produce a new recursive
    list.

    >>> evens = rlist(2, rlist(4, rlist(6, rlist(8, empty_rlist))))
    >>> odds = rlist(1, rlist(3, empty_rlist))
    >>> interleave_recursive(odds, evens)
    (1, (2, (3, (4, (6, (8, None))))))
    >>> interleave_recursive(evens, odds)
    (2, (1, (4, (3, (6, (8, None))))))
    >>> interleave_recursive(odds, odds)
    (1, (1, (3, (3, None))))
    """
    "*** YOUR CODE HERE ***"
     # a helper functin that joins two rlist using rest(), first() and rlist()  
    def join(a, b):                                                                                 
        a = reverse_rlist_recursive(a)                                                              
        while a != empty_rlist:
            a, b = rest(a), rlist(first(a), b)                                                      
        return b                                                                                    
                  
    def helper(s0, s1, newlist):
        if s0 == empty_rlist: return join(newlist, s1)
        if s1 == empty_rlist: return join(newlist, s0)
        newlist = join(newlist, rlist(s0[0], empty_rlist)) 
        newlist = join(newlist, rlist(s1[0], empty_rlist))
        return helper(rest(s0), rest(s1), newlist)
        
    return helper(rest(s0), rest(s1), rlist(s0[0], rlist(s1[0], empty_rlist)))





        
def interleave_iterative(s0, s1):
    """Interleave recursive lists s0 and s1 to produce a new recursive
    list.

    >>> evens = rlist(2, rlist(4, rlist(6, rlist(8, empty_rlist))))
    >>> odds = rlist(1, rlist(3, empty_rlist))
    >>> interleave_iterative(odds, evens)
    (1, (2, (3, (4, (6, (8, None))))))
    >>> interleave_iterative(evens, odds)
    (2, (1, (4, (3, (6, (8, None))))))
    >>> interleave_iterative(odds, odds)
    (1, (1, (3, (3, None))))
    """
    "*** YOUR CODE HERE ***"
    # a helper functin that joins two rlist using rest(), first() and rlist()
    def join(a, b):
        a = reverse_rlist_recursive(a)
        while a != empty_rlist:
            a, b = rest(a), rlist(first(a), b)
        return b 

    newlist = join( rlist(s0[0], empty_rlist), rlist(s1[0], empty_rlist))
    s0, s1 = rest(s0), rest(s1)

    while s0 != empty_rlist and s1 != empty_rlist:
        newlist = join(newlist, rlist(s0[0], empty_rlist))
        newlist = join(newlist, rlist(s1[0], empty_rlist))
        s0, s1 = rest(s0), rest(s1)

    if s0 == empty_rlist:
        return join(newlist, s1)
    if s1 == empty_rlist:
        return join(newlist, s0)

def str_interval(x):
    """Return a string representation of interval x.

    >>> str_interval(interval(-1, 2))
    '-1 to 2'
    """
    return '{0} to {1}'.format(lower_bound(x), upper_bound(x))

def add_interval(x, y):
    """Return an interval that contains the sum of any value in interval x and
    any value in interval y.

    >>> str_interval(add_interval(interval(-1, 2), interval(4, 8)))
    '3 to 10'
    """
    lower = lower_bound(x) + lower_bound(y)
    upper = upper_bound(x) + upper_bound(y)
    return interval(lower, upper)

def mul_interval(x, y):
    """Return the interval that contains the product of any value in x and any
    value in y.

    >>> str_interval(mul_interval(interval(-1, 2), interval(4, 8)))
    '-8 to 16'
    """
    p1 = lower_bound(x) * lower_bound(y)
    p2 = lower_bound(x) * upper_bound(y)
    p3 = upper_bound(x) * lower_bound(y)
    p4 = upper_bound(x) * upper_bound(y)
    return interval(min(p1, p2, p3, p4), max(p1, p2, p3, p4))


# Q3.

def interval(a, b):
    """Construct an interval from a to b."""
    "*** YOUR CODE HERE ***"
    return (a, b)

def lower_bound(x):
    """Return the lower bound of interval x."""
    "*** YOUR CODE HERE ***"
    return x[0]

def upper_bound(x):
    """Return the upper bound of interval x."""
    "*** YOUR CODE HERE ***"
    return x[1]

# Q4.

def div_interval(x, y):
    """Return the interval that contains the quotient of any value in x
    divided by any value in y.

    Division is implemented as the multiplication of x by the reciprocal of y.

    >>> str_interval(div_interval(interval(-1, 2), interval(4, 8)))
    '-0.25 to 0.5'
    """
    "*** YOUR CODE HERE ***"
    assert not (lower_bound(y) <= 0 and upper_bound(y) >= 0), "Interval y contains 0."
    reciprocal_y = interval(1/upper_bound(y), 1/lower_bound(y))
    return mul_interval(x, reciprocal_y)

# Q5.

def sub_interval(x, y):
    """Return the interval that contains the difference between any value in x
    and any value in y.

    >>> str_interval(sub_interval(interval(-1, 2), interval(4, 8)))
    '-9 to -2'
    """
    "*** YOUR CODE HERE ***"
    return interval(lower_bound(x) - upper_bound(y), upper_bound(x) - lower_bound(y))

# Q6.

def make_center_width(c, w):
    """Construct an interval from center and width."""
    return interval(c - w, c + w)

def center(x):
    """Return the center of interval x."""
    return (upper_bound(x) + lower_bound(x)) / 2

def width(x):
    """Return the width of interval x."""
    return (upper_bound(x) - lower_bound(x)) / 2


def make_center_percent(c, p):
    """Construct an interval from center and percentage tolerance.

    >>> str_interval(make_center_percent(2, 50))
    '1.0 to 3.0'
    """
    "*** YOUR CODE HERE ***"
    w = abs( c * p / 100 )
    return make_center_width(c, w)

def percent(x):
    """Return the percentage tolerance of interval x.

    >>> percent(interval(1, 3))
    50.0
    """
    "*** YOUR CODE HERE ***"
    a, b = lower_bound(x), upper_bound(x)
    w = (b - a) /2
    c = (b + a) /2
    return abs(w / c) * 100

# Q7.

def quadratic(x, a, b, c):
    """Return the interval that is the range the quadratic defined by a, b,
    and c, for domain interval x.

    This is the less accurate version which treats each instance of t as a
    different value from the interval. See the extra for experts question for
    exploring why this is not _really_ correct and to write a more precise
    version.

    >>> str_interval(quadratic(interval(0, 2), -2, 3, -1))
    '-9 to 5'
    >>> str_interval(quadratic(interval(1, 3), 2, -3, 1))
    '-6 to 16'
    """
    "*** YOUR CODE HERE ***"
    tt = mul_interval(x, x)
    att_lower = min(a * lower_bound(tt), a* upper_bound(tt))
    att_upper = max(a * lower_bound(tt), a* upper_bound(tt))
    att = interval(att_lower, att_upper)

    bt_lower = min(b * lower_bound(x), b * upper_bound(x))
    bt_upper = max(b * lower_bound(x), b * upper_bound(x))  
    bt = interval(bt_lower, bt_upper)
    
    attbt = add_interval(att, bt)
  
    return interval(c + lower_bound(attbt), c + upper_bound(attbt))

# Q8.

def par1(r1, r2):
    return div_interval(mul_interval(r1, r2), add_interval(r1, r2))

def par2(r1, r2):
    one = interval(1, 1)
    rep_r1 = div_interval(one, r1)
    rep_r2 = div_interval(one, r2)
    return div_interval(one, add_interval(rep_r1, rep_r2))


# These two intervals give different results for parallel resistors:
"*** YOUR CODE HERE ***"
a = interval(1,100)
b = interval(1, 1000)

# Q9.

def multiple_reference_explanation():
  return "each calculation involving uncertainty will (in general) make the uncertainty larger. so we can avoid unnecessary accumulation of error by limiting the number of element calculations. so if we do not repeat the same value in calculation, we get a smaller error"

# Q10.

def accurate_quadratic(x, a, b, c):
    """Return the interval that is the range the quadratic defined by a, b,
    and c, for domain interval x.

    >>> str_interval(accurate_quadratic(interval(0, 2), -2, 3, -1))
    '-3 to 0.125'
    >>> str_interval(accurate_quadratic(interval(1, 3), 2, -3, 1))
    '0 to 10'
    """
    "*** YOUR CODE HERE ***"
    def f(x):
        return a * x * x + b * x + c
    left, middle, right = lower_bound(x), - b / (2 * a), upper_bound(x)
    if middle <= left or middle >=right:
        maximum, minimum = max(f(left), f(right)), min(f(left), f(right))
    else:
        maximum, minimum = max(f(left),f(middle), f(right)), min(f(left),f(middle), f(right))
    return interval(minimum, maximum)

