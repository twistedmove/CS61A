# Name: Hanyu Zhang
# Login: cs61a-pb
# TA: Richard
# Section: 112
# Q1.

def smooth(f, dx):
    """Returns the smoothed version of f, g where

    g(x) = (f(x - dx) + f(x) + f(x + dx)) / 3

    >>> square = lambda x: x ** 2
    >>> round(smooth(square, 1)(0), 3)
    0.667
    """
    "*** YOUR CODE HERE ***"
    return lambda x: (f(x - dx) + f(x) + f(x + dx)) / 3

def repeated(f, n):
    """Return the function that computes the nth application of f.
        
        f -- a function that takes one argument
        n -- a positive integer
        
        """
    g = f
    while n > 1:
        g = compose1(f, g)
        n = n - 1
    return g

def compose1(f, g):
    """Return a function h, such that h(x) = f(g(x))."""
    def h(x):
         return f(g(x))
    return h

def n_fold_smooth(f, dx, n):
    """Returns the n-fold smoothed version of f

    >>> square = lambda x: x ** 2
    >>> round(n_fold_smooth(square, 1, 3)(0), 3)
    2.0
    """
    "*** YOUR CODE HERE ***"
    fixed_smooth = repeated(lambda x: smooth(x, dx), n)
    return fixed_smooth(f)

    
# Q2.

def iterative_continued_frac(n_term, d_term, k):
    """Returns the k-term continued fraction with numerators defined by n_term
    and denominators defined by d_term.

    >>> # golden ratio
    ... round(iterative_continued_frac(lambda x: 1, lambda x: 1, 8), 3)
    0.618
    >>> # 1 / (1 + (2 / (2 + (3 / (3 + (4 / 4))))))
    ... round(iterative_continued_frac(lambda x: x, lambda x: x, 4), 6)
    0.578947
    """
    "*** YOUR CODE HERE ***"
    d_k = d_term(k)
    while k >= 1:
        d_k = d_term(k-1) + n_term(k) / d_k
        k = k - 1
    return d_k - d_term(0)


def recursive_continued_frac(n_term, d_term, k):
    """Returns the k-term continued fraction with numerators defined by n_term
    and denominators defined by d_term.

    >>> # golden ratio
    ... round(recursive_continued_frac(lambda x: 1, lambda x: 1, 8), 3)
    0.618
    >>> # 1 / (1 + (2 / (2 + (3 / (3 + (4 / 4))))))
    ... round(recursive_continued_frac(lambda x: x, lambda x: x, 4), 6)
    0.578947
    """
    "*** YOUR CODE HERE ***"
    def helper(n):
        if n == 1:
            return n_term(k) / d_term(k)
        else:
            return n_term(k-n+1) / (d_term(k-n+1) + helper(n-1))
    return helper(k)

# Q3.

def g(n):
    """Return the value of G(n), computed recursively.

    >>> g(1)
    1
    >>> g(2)
    2
    >>> g(3)
    3
    >>> g(4)
    10
    >>> g(5)
    22
    """
    "*** YOUR CODE HERE ***"
    if n <= 3:
        return n
    return g(n-1) + 2 * g(n-2) + 3 * g(n-3)

def g_iter(n):
    """Return the value of G(n), computed iteratively.
    >>> g_iter(1)
    1
    >>> g_iter(2)
    2
    >>> g_iter(3)
    3
    >>> g_iter(4)
    10
    >>> g_iter(5)
    22
    """
    "*** YOUR CODE HERE ***"
    if n <= 3:
        return n
    first, second, third = 1, 2, 3
    for i in range(0, n - 3):
        first, second, third = second, third, 3 * first + 2 * second + third
    return third

# Q4.

from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    """
    return lambda i : (lambda f,g:f(f,g)) ( (lambda f,x: 1 if x == 0 else x * f(f,x-1)) ,i)


