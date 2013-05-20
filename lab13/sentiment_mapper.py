#!/usr/bin/env python3

import sys
from ucb import main
from mr import emit

from trends import extract_words, get_word_sentiment, has_sentiment, sentiment_value
from mr import get_file

@main
def run():
    """
    For each line you are supplied, you should break it up into words, 
    find the sentiment of these words, and return the average sentiment
    of the words that have sentiment (don't count words without sentiment).
    Return 0 if no words have sentiment.
    """
    for line in sys.stdin:
        """***YOUR CODE HERE***"""
        