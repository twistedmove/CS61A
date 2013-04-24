# Name: Hanyu Zhang
# Login: cs61a-pb
# TA: Richard
# Section: 112
# Q1.

def pig_latin_original(w):
    """Return the Pig Latin equivalent of a lowercase English word w."""
    if starts_with_a_vowel(w):
        return w + 'ay'
    return pig_latin(rest(w) + first(w))

def first(s):
    """Returns the first character of a string."""
    return s[0]

def rest(s):
    """Returns all but the first character of a string."""
    return s[1:]

def starts_with_a_vowel(w):
    """Return whether w begins with a vowel."""
    c = first(w)
    return c == 'a' or c == 'e' or c == 'i' or c == 'o' or c == 'u'


def pig_latin(w):
    """Return the Pig Latin equivalent of a lowercase English word w.

    >>> pig_latin('pun')
    'unpay'
    >>> pig_latin('sphynx')
    'sphynxay'
    """
    "*** YOUR CODE HERE ***"
    def helper(w, k):
        if k == 0 or starts_with_a_vowel(w):
            return w + 'ay'
        return helper(rest(w) + w[0], k-1)
    return helper(w, len(w))
    

# Q2.

def towers_of_hanoi(n, start, end):
    """Print the moves required to solve the towers of hanoi game if we start
    with n disks on the start pole and want to move them all to the end pole.

    The game is to assumed to have 3 poles (which is traditional).

    >>> towers_of_hanoi(1, 1, 3)
    Move 1 disk from rod 1 to rod 3
    >>> towers_of_hanoi(2, 1, 3)
    Move 1 disk from rod 1 to rod 2
    Move 1 disk from rod 1 to rod 3
    Move 1 disk from rod 2 to rod 3
    >>> towers_of_hanoi(3, 1, 3)
    Move 1 disk from rod 1 to rod 3
    Move 1 disk from rod 1 to rod 2
    Move 1 disk from rod 3 to rod 2
    Move 1 disk from rod 1 to rod 3
    Move 1 disk from rod 2 to rod 1
    Move 1 disk from rod 2 to rod 3
    Move 1 disk from rod 1 to rod 3
    """
    "*** YOUR CODE HERE ***"
    def move(n, start, end, extra):
        if n == 1: 
           move_disk(start, end)
           return
        move(n - 1, start, extra, end)
        move_disk(start, end)
        move(n - 1, extra, end, start)
    move(n, start, end, 2)


def move_disk(start, end):
    print("Move 1 disk from rod", start, "to rod", end)

# Q3.

def part(n):
    """Return the number of partitions of positive integer n.

    >>> part(5)
    7
    >>> part(10)
    42
    >>> part(15)
    176
    >>> part(20)
    627
    """
    "*** YOUR CODE HERE ***"
    k = n
    def helper(n, k):
         if n == 0: return 1
         if k == 0 or n < 0: return 0
         return helper(n - k, k) + helper(n, k - 1)
    return helper(n, k)
# Q4.

def summation(n, term):
    """Return the sum of the first n terms of a sequence.
  
    >>> summation(5, lambda x: pow(x, 3))
    225
    """
    total, k = 0, 1
    while k <= n:
        total, k = total + term(k), k + 1
    return total


def interleaved_sum(n, odd_term, even_term):
    """Compute the sum odd_term(1) + even_term(2) + odd_term(3) + ..., up
    to n.

    >>> # 1 + 2^2 + 3 + 4^2 + 5
    ... interleaved_sum(5, lambda x: x, lambda x: x*x)
    29
    """
    "*** YOUR CODE HERE ***"
    newterm = lambda oldterm: odd_term if oldterm == even_term else even_term
    def helper(term, k):
        if k == n: return term(k)
        return term(k) + helper(newterm(term), k + 1)
    return helper(odd_term, 1)
