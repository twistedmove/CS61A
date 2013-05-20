#!/usr/bin/env python3

import sys
from ucb import main
from mr import values_by_key, emit

@main
def run():
    for key, value_iterator in values_by_key(sys.stdin):
        emit(key, sum(value_iterator))
