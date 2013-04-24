# Name: Hanyu Zhang
# Login: cs61a-pb
# TA: Richard
# Section: 112
# Q1.

def divide_by_fact(dividend, n):
    """Recursively divide dividend by the factorial of n.

    >>> divide_by_fact(120, 4)
    5.0
    """
    if n == 0:
    	return dividend
    return divide_by_fact(dividend / n, n - 1)

# Q2.

def group(seq):
    """Divide a sequence of at least 12 elements into groups of 4 or
    5. Groups of 5 will be at the end. Returns a tuple of sequences, each
    corresponding to a group.

    >>> group(range(14))
    (range(0, 4), range(4, 9), range(9, 14))
    >>> group(tuple(range(17)))
    ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15, 16))
    """
    num = len(seq)
    assert num >= 12
    "*** YOUR CODE HERE ***"
    def split(alist, n):
        if n == 0: return alist
        if n == 15 or n == 10 or n == 5:  
            return alist + [5] * (n//5)
        return split(alist + [4], n-4)

    list_of_number = split([], num)
    new_group = []
    for i in list_of_number:
        new_group.append(seq[0: i ])
        seq = seq[i: ]
    return tuple(new_group)
        

"""

   ====
    ==
========== <--- spatula underneath this crust
 ========

    ||
    ||
   \||/
    \/

========== }
    ==     } flipped
   ====    }
 ========

"""

# Q3.

def partial_reverse(lst, start):
    """Reverse part of a list in-place, starting with start up to the end of
    the list.

    >>> a = [1, 2, 3, 4, 5, 6, 7]
    >>> partial_reverse(a, 2)
    >>> a
    [1, 2, 7, 6, 5, 4, 3]
    >>> partial_reverse(a, 5)
    >>> a
    [1, 2, 7, 6, 5, 3, 4]
    """
    "*** YOUR CODE HERE ***"
    for _ in lst[start: ]:
        lst.insert(start, _)
        lst.pop()
# Q4.

def index_largest(seq):
    """Return the index of the largest element in the sequence.

    >>> index_largest([8, 5, 7, 3 ,1])
    0
    >>> index_largest((4, 3, 7, 2, 1))
    2
    """
    assert len(seq) > 0
    "*** YOUR CODE HERE ***"
    return seq.index(max(seq))

# Q5.

def pizza_sort(lst):
    """Perform an in-place pizza sort on the given list, resulting in
    elements in descending order.

    >>> a = [8, 5, 7, 3, 1, 9, 2]
    >>> pizza_sort(a)
    >>> a
    [9, 8, 7, 5, 3, 2, 1]
    """
    "*** YOUR CODE HERE ***"
    for i in range(0, len(lst)):
        if index_largest(lst[i:]) + i  != len(lst) -1:
           partial_reverse(lst, index_largest(lst[i:]) + i)
        partial_reverse(lst, i)

# Q6.

def make_accumulator():
    """Return an accumulator function that takes a single numeric argument and
    accumulates that argument into total, then returns total.

    >>> acc = make_accumulator()
    >>> acc(15)
    15
    >>> acc(10)
    25
    >>> acc2 = make_accumulator()
    >>> acc2(7)
    7
    >>> acc3 = acc2
    >>> acc3(6)
    13
    >>> acc2(5)
    18
    >>> acc(4)
    29
    """
    "*** YOUR CODE HERE ***"
    things = []
    def acc(a_thing):
        things.append(a_thing)
        return sum(things)
    return acc


# Q7.

def make_accumulator_nonlocal():
    """Return an accumulator function that takes a single numeric argument and
    accumulates that argument into total, then returns total.

    >>> acc = make_accumulator_nonlocal()
    >>> acc(15)
    15
    >>> acc(10)
    25
    >>> acc2 = make_accumulator_nonlocal()
    >>> acc2(7)
    7
    >>> acc3 = acc2
    >>> acc3(6)
    13
    >>> acc2(5)
    18
    >>> acc(4)
    29
    """
    "*** YOUR CODE HERE ***"
    total = 0
    def acc(n):
        nonlocal total
        total = total + n
        return total
    return acc


# Q8.

# Old version
def count_change(a, coins=(50, 25, 10, 5, 1)):
    if a == 0:
        return 1
    elif a < 0 or len(coins) == 0:
        return 0
    return count_change(a, coins[1:]) + count_change(a - coins[0], coins)

# Version 2.0
lib = {}

def make_count_change():
    """Return a function to efficiently count the number of ways to make
    change.

    >>> cc = make_count_change()
    >>> cc(500, (50, 25, 10, 5, 1))
    59576
    """
    "*** YOUR CODE HERE ***"
    lib = {}
    def count_change(a, coins=(50, 25, 10, 5, 1)):
        if a == 0:
            return 1
        elif a < 0 or len(coins) == 0:
            return 0
        if a not in lib: lib[a]={}
        if len(coins) not in lib[a]:
               cache = {} 
               cache[len(coins)] = count_change(a, coins[1:]) + count_change(a - coins[0], coins)
               lib[a].update(cache)
        return lib[a][len(coins)]

    def cc(a, coins=(50, 25, 10, 5, 1)):
        # avoid reaching max recursion depth; break into steps instead
        
        for i in range(0, a, 950): count_change(i, coins)
        return count_change(a,coins)



        
    return cc


