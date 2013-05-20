"""Visualizing Twitter Sentiment Across America"""

from data import word_sentiments
from string import ascii_letters
from ucb import main, trace, interact, log_current_line

def extract_words(text):
    """Return the words in a string.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    """
    # BEGIN SOLUTION ALT="return text.split()  # Replace"
    words = []
    current_word = ''
    for c in text:
        if c not in ascii_letters:
            words.append(current_word)
            current_word = ''
        else:
            current_word += c
    words.append(current_word)
    return list(filter(lambda w: len(w)>0, words))
    # END SOLUTION

def make_sentiment(value):
    """Return a sentiment, which represents a value that may not exist.

    >>> s = make_sentiment(0.2)
    >>> t = make_sentiment(None)
    >>> has_sentiment(s)
    True
    >>> has_sentiment(t)
    False
    >>> sentiment_value(s)
    0.2
    """
    assert value is None or (value >= -1 and value <= 1), 'Illegal value'
    # BEGIN SOLUTION
    return value
    # END SOLUTION

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    # BEGIN SOLUTION
    return s is not None
    # END SOLUTION

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    # BEGIN SOLUTION
    return s
    # END SOLUTION

def get_word_sentiment(word):
    """Return a sentiment representing the degree of positive or negative
    feeling in the given word.

    >>> sentiment_value(get_word_sentiment('good'))
    0.875
    >>> sentiment_value(get_word_sentiment('bad'))
    -0.625
    >>> sentiment_value(get_word_sentiment('winning'))
    0.5
    >>> has_sentiment(get_word_sentiment('Berkeley'))
    False
    """
    return make_sentiment(word_sentiments.get(word, None))
