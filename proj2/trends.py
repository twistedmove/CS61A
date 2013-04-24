"""Visualizing Twitter Sentiment Across America"""

from data import word_sentiments, load_tweets
from datetime import datetime
from doctest import run_docstring_examples
from geo import us_states, geo_distance, make_position, longitude, latitude
from maps import draw_state, draw_name, draw_dot, wait, message
from string import ascii_letters
from ucb import main, trace, interact, log_current_line


# Phase 1: The Feelings in Tweets

def make_tweet(text, time, lat, lon):
    """Return a tweet, represented as a python dictionary.

    text      -- A string; the text of the tweet, all in lowercase
    time      -- A datetime object; the time that the tweet was posted
    latitude  -- A number; the latitude of the tweet's location
    longitude -- A number; the longitude of the tweet's location

    >>> t = make_tweet("just ate lunch", datetime(2012, 9, 24, 13), 38, 74)
    >>> tweet_words(t)
    ['just', 'ate', 'lunch']
    >>> tweet_time(t)
    datetime.datetime(2012, 9, 24, 13, 0)
    >>> p = tweet_location(t)
    >>> latitude(p)
    38
    """
    return {'text': text, 'time': time, 'latitude': lat, 'longitude': lon}

def tweet_words(tweet):
    """Return a list of the words in the text of a tweet."""
    "*** YOUR CODE HERE ***"
    return extract_words(tweet['text'])

def tweet_time(tweet):
    """Return the datetime that represents when the tweet was posted."""
    "*** YOUR CODE HERE ***"
    return tweet['time']


def tweet_location(tweet):
    """Return a position (see geo.py) that represents the tweet's location."""
    "*** YOUR CODE HERE ***"
    return make_position(tweet['latitude'], tweet['longitude'])
    

def tweet_string(tweet):
    """Return a string representing the tweet."""
    return '"{0}" @ {1}'.format(tweet['text'], tweet_location(tweet))

def extract_words(text):
    """Return the words in a tweet, not including punctuation.

    >>> extract_words('anything else.....not my job')
    ['anything', 'else', 'not', 'my', 'job']
    >>> extract_words('i love my job. #winning')
    ['i', 'love', 'my', 'job', 'winning']
    >>> extract_words('make justin # 1 by tweeting #vma #justinbieber :)')
    ['make', 'justin', 'by', 'tweeting', 'vma', 'justinbieber']
    >>> extract_words("paperclips! they're so awesome, cool, & useful!")
    ['paperclips', 'they', 're', 'so', 'awesome', 'cool', 'useful']
    """
    "*** YOUR CODE HERE ***"
    #return text.split()  
    # if the input is not a single letter [a-zA-z] then return ' ' else return the input letter
    replace = lambda letter: letter if letter.isalpha() else ' '
    raw = text.split()
    result = []
    for word in raw:
        # split word into letters, replace non-letters with a space. join the letters, then split.
        split_word=(''.join( [ replace(word[i]) for i in range(0, len(word)) ])).split()
        for new_word in split_word:
            result.append(new_word)
    return result


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
    "*** YOUR CODE HERE ***"
    # store the sentiment in a single-element list
    return [value]

def has_sentiment(s):
    """Return whether sentiment s has a value."""
    "*** YOUR CODE HERE ***"
    return s[0] != None

def sentiment_value(s):
    """Return the value of a sentiment s."""
    assert has_sentiment(s), 'No sentiment value'
    "*** YOUR CODE HERE ***"
    return s[0]

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

def analyze_tweet_sentiment(tweet):
    """ Return a sentiment representing the degree of positive or negative
    sentiment in the given tweet, averaging over all the words in the tweet
    that have a sentiment value.

    If no words in the tweet have a sentiment value, return
    make_sentiment(None).

    >>> positive = make_tweet('i love my job. #winning', None, 0, 0)
    >>> round(sentiment_value(analyze_tweet_sentiment(positive)), 5)
    0.29167
    >>> negative = make_tweet("saying, 'i hate my job'", None, 0, 0)
    >>> sentiment_value(analyze_tweet_sentiment(negative))
    -0.25
    >>> no_sentiment = make_tweet("berkeley golden bears!", None, 0, 0)
    >>> has_sentiment(analyze_tweet_sentiment(no_sentiment))
    False
    """
    average = make_sentiment(None)
    "*** YOUR CODE HERE ***"
    # filter out tweets with no sentiment
    words_with_sentiment = [ word for word in tweet_words(tweet) if
                             has_sentiment(get_word_sentiment(word)) ] 
    # if no words in the tweet have a sentiment value                         
    if len(words_with_sentiment) == 0: return make_sentiment(None)

    total_value = sum([sentiment_value(get_word_sentiment(value)) for value in  words_with_sentiment])
    return make_sentiment(total_value / len(words_with_sentiment ))


# Phase 2: The Geometry of Maps

def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, return its first position as its centroid

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> find_centroid(triangle)
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p3, p2, p1])
    (3.0, 2.0, 6.0)
    >>> tuple(map(float, find_centroid([p1, p2, p1]))) # Forces result to be floats
    (1.0, 2.0, 0.0)
    """
    "*** YOUR CODE HERE ***"
    n = len(polygon) - 1 # number of vertices
    # list of all x coordinates and list of all y coordinates
    x_list = [ location[0] for location in polygon]
    y_list = [ location[1] for location in polygon] 

    # signed area 
    A = 1/2 *sum([(x_list[i] * y_list[i+1] - x_list[i+1] * y_list[i]) for i in range(0, n)])
    if A == 0: return polygon[0][0], polygon[0][1], 0
    cx = 1 / (6 * A)* sum([(x_list[i] + x_list[i+1]) * (x_list[i] * y_list[i+1] - x_list[i+1] * y_list[i]) for i in range(0,n)])
    cy = 1 / (6 * A)* sum([(y_list[i] + y_list[i+1]) * (x_list[i] * y_list[i+1] - x_list[i+1] * y_list[i]) for i in range(0,n)])
    return (cx, cy, abs(A))

def find_center(polygons):
    """Compute the geographic center of a state, averaged over its polygons.

    The center is the average position of centroids of the polygons in polygons,
    weighted by the area of those polygons.

    Arguments:
    polygons -- a list of polygons

    >>> ca = find_center(us_states['CA'])  # California
    >>> round(latitude(ca), 5)
    37.25389
    >>> round(longitude(ca), 5)
    -119.61439

    >>> hi = find_center(us_states['HI'])  # Hawaii
    >>> round(latitude(hi), 5)
    20.1489
    >>> round(longitude(hi), 5)
    -156.21763
    """
    "*** YOUR CODE HERE ***"
    x = lambda polygon: find_centroid(polygon)[0]  # x getter
    y = lambda polygon: find_centroid(polygon)[1]  # y getter
    A = lambda polygon: find_centroid(polygon)[2]  # area getter
    total_area = sum([A(polygon) for polygon in polygons])
    Cx = sum([x(polygon) * A(polygon) for polygon in polygons]) / total_area 
    Cy = sum([y(polygon) * A(polygon) for polygon in polygons]) / total_area  
    return Cx, Cy



# Phase 3: The Mood of the Nation

def find_closest_state(tweet, state_centers):
    """Return the name of the state closest to the given tweet's location.

    Use the geo_distance function (already provided) to calculate distance
    in miles between two latitude-longitude positions.

    Arguments:
    tweet -- a tweet abstract data type
    state_centers -- a dictionary from state names to positions.

    >>> us_centers = {n: find_center(s) for n, s in us_states.items()}
    >>> sf = make_tweet("welcome to san Francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new York", None, 41, -74)
    >>> find_closest_state(sf, us_centers)
    'CA'
    >>> find_closest_state(ny, us_centers)
    'NJ'
    """
    "*** YOUR CODE HERE ***"
    location = tweet_location(tweet)
    # a dictionary of state name and it's distance to the tweet's location
    distances = {name: geo_distance(state_centers[name], location) for name in state_centers}
    min_distance = min([distances[name] for name in distances])
    for name in distances:
        if distances[name] == min_distance: return name

def group_tweets_by_state(tweets):
    """Return a dictionary that aggregates tweets by their nearest state center.

    The keys of the returned dictionary are state names, and the values are
    lists of tweets that appear closer to that state center than any other.

    tweets -- a sequence of tweet abstract data types

    >>> sf = make_tweet("welcome to san francisco", None, 38, -122)
    >>> ny = make_tweet("welcome to new york", None, 41, -74)
    >>> ca_tweets = group_tweets_by_state([sf, ny])['CA']
    >>> tweet_string(ca_tweets[0])
    '"welcome to san francisco" @ (38, -122)'
    """
    tweets_by_state = {}
    "*** YOUR CODE HERE ***"
    state_centers = {n: find_center(s) for n, s in us_states.items()}  # dictionary of all state: state center
    states_list = [ find_closest_state(tweet, state_centers) for tweet in tweets ]  # list of all states in tweets
    states = set(states_list) # set of all state_names involved in tweets, with repeated state_names removed
    # list_of_tweet_from(state_name) returns a list of all tweets from a given state_name
    list_of_tweet_from = lambda state_name: [tweet for tweet in tweets if find_closest_state(tweet, state_centers) == state_name ] 
    tweets_by_state = {state: list_of_tweet_from(state)  for state  in states  }
    return tweets_by_state

def most_talkative_state(term):
    """Return the state that has the largest number of tweets containing term.

    >>> most_talkative_state('texas')
    'TX'
    >>> most_talkative_state('soup')
    'CA'
    """
    tweets = load_tweets(make_tweet, term)  # A list of tweets containing term
    "*** YOUR CODE HERE ***"
    group = group_tweets_by_state(tweets)
    number_of_most_mentioned = max([len(group[i]) for i in group])
    for some_state in group:
        if len(group[some_state]) == number_of_most_mentioned:
            return some_state

def average_sentiments(tweets_by_state):
    """Calculate the average sentiment of the states by averaging over all
    the tweets from each state. Return the result as a dictionary from state
    names to average sentiment values (numbers).

    If a state has no tweets with sentiment values, leave it out of the
    dictionary entirely.  Do NOT include states with no tweets, or with tweets
    that have no sentiment, as 0.  0 represents neutral sentiment, not unknown
    sentiment.

    tweets_by_state -- A dictionary from state names to lists of tweets
    """
    averaged_state_sentiments = {}
    "*** YOUR CODE HERE ***"
    def average(alist):
        # return the the average of numbers in a list
        return sum(alist)/len(alist)

    def analyze_tweet_list_sentiment(list_of_tweet):
        # input is a list of tweet objects; 
        # output is a sentiment object with the average sentiment value
        all_none = True
        list_of_sentiment = []
        for tweet in list_of_tweet:
            if has_sentiment(analyze_tweet_sentiment(tweet)):
               list_of_sentiment.append(analyze_tweet_sentiment(tweet))
               all_none = False
        if all_none: return make_sentiment(None) # return None if all tweets in the list has sentiment == None
        list_of_sentiment_value = [sentiment_value(sentiment) for sentiment in list_of_sentiment]

        return make_sentiment(average(list_of_sentiment_value))
    
    # construct averaged_state_sentiments
    for state in tweets_by_state:
        ave = analyze_tweet_list_sentiment(tweets_by_state[state])
        if has_sentiment(ave):
           averaged_state_sentiments[state] = sentiment_value(ave)

    return averaged_state_sentiments


# Phase 4: Into the Fourth Dimension

def group_tweets_by_hour(tweets):
    """Return a dictionary that groups tweets by the hour they were posted.

    The keys of the returned dictionary are the integers 0 through 23.

    The values are lists of tweets, where tweets_by_hour[i] is the list of all
    tweets that were posted between hour i and hour i + 1. Hour 0 refers to
    midnight, while hour 23 refers to 11:00PM.

    To get started, read the Python Library documentation for datetime objects:
    http://docs.python.org/py3k/library/datetime.html#datetime.datetime

    tweets -- A list of tweets to be grouped

    >>> tweets = load_tweets(make_tweet, 'party')
    >>> tweets_by_hour = group_tweets_by_hour(tweets)
    >>> for hour in [0, 5, 9, 17, 23]:
    ...     current_tweets = tweets_by_hour.get(hour, [])
    ...     tweets_by_state = group_tweets_by_state(current_tweets)
    ...     state_sentiments = average_sentiments(tweets_by_state)
    ...     print('HOUR:', hour)
    ...     for state in ['CA', 'FL', 'DC', 'MO', 'NY']:
    ...         if state in state_sentiments.keys():
    ...             print(state, ":", round(state_sentiments[state], 5))
    HOUR: 0
    CA : 0.08333
    FL : -0.09635
    DC : 0.01736
    MO : -0.11979
    NY : -0.15
    HOUR: 5
    CA : 0.00945
    FL : -0.0651
    DC : 0.03906
    MO : 0.1875
    NY : -0.04688
    HOUR: 9
    CA : 0.10417
    NY : 0.25
    HOUR: 17
    CA : 0.09808
    FL : 0.0875
    MO : -0.1875
    NY : 0.14583
    HOUR: 23
    CA : -0.10729
    FL : 0.01667
    DC : -0.3
    MO : -0.0625
    NY : 0.21875
    """
    tweets_by_hour = {}
    "*** YOUR CODE HERE ***"
    for i in range(0,24): tweets_by_hour[i] = []  # initialize

    for tweet in tweets:
        hour = tweet['time'].hour
        tweets_by_hour[hour].append(tweet)

    return tweets_by_hour


# Interaction.  You don't need to read this section of the program.

def print_sentiment(text='Are you virtuous or verminous?'):
    """Print the words in text, annotated by their sentiment scores."""
    words = extract_words(text.lower())
    layout = '{0:>' + str(len(max(words, key=len))) + '}: {1:+}'
    for word in words:
        s = get_word_sentiment(word)
        if has_sentiment(s):
            print(layout.format(word, sentiment_value(s)))

def draw_centered_map(center_state='TX', n=10):
    """Draw the n states closest to center_state."""
    us_centers = {n: find_center(s) for n, s in us_states.items()}
    center = us_centers[center_state.upper()]
    dist_from_center = lambda name: geo_distance(center, us_centers[name])
    for name in sorted(us_states.keys(), key=dist_from_center)[:int(n)]:
        draw_state(us_states[name])
        draw_name(name, us_centers[name])
    draw_dot(center, 1, 10)  # Mark the center state with a red dot
    wait()

def draw_state_sentiments(state_sentiments={}):
    """Draw all U.S. states in colors corresponding to their sentiment value.

    Unknown state names are ignored; states without values are colored grey.

    state_sentiments -- A dictionary from state strings to sentiment values
    """
    for name, shapes in us_states.items():
        sentiment = state_sentiments.get(name, None)
        draw_state(shapes, sentiment)
    for name, shapes in us_states.items():
        center = find_center(shapes)
        if center is not None:
            draw_name(name, center)

def draw_map_for_term(term='my job'):
    """Draw the sentiment map corresponding to the tweets that contain term.

    Some term suggestions:
    New York, Texas, sandwich, my life, justinbieber
    """
    tweets = load_tweets(make_tweet, term)
    tweets_by_state = group_tweets_by_state(tweets)
    state_sentiments = average_sentiments(tweets_by_state)
    draw_state_sentiments(state_sentiments)
    for tweet in tweets:
        s = analyze_tweet_sentiment(tweet)
        if has_sentiment(s):
            draw_dot(tweet_location(tweet), sentiment_value(s))
    wait()

def draw_map_by_hour(term='my job', pause=0.5):
    """Draw the sentiment map for tweets that match term, for each hour."""
    tweets = load_tweets(make_tweet, term)
    tweets_by_hour = group_tweets_by_hour(tweets)

    for hour in range(24):
        current_tweets = tweets_by_hour.get(hour, [])
        tweets_by_state = group_tweets_by_state(current_tweets)
        state_sentiments = average_sentiments(tweets_by_state)
        draw_state_sentiments(state_sentiments)
        message("{0:02}:00-{0:02}:59".format(hour))
        wait(pause)

def run_doctests(names):
    """Run verbose doctests for all functions in space-separated names."""
    g = globals()
    errors = []
    for name in names.split():
        if name not in g:
            print("No function named " + name)
        else:
            run_docstring_examples(g[name], g, True, name)

@main
def run(*args):
    """Read command-line arguments and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Run Trends")
    parser.add_argument('--print_sentiment', '-p', action='store_true')
    parser.add_argument('--run_doctests', '-t', action='store_true')
    parser.add_argument('--draw_centered_map', '-d', action='store_true')
    parser.add_argument('--draw_map_for_term', '-m', action='store_true')
    parser.add_argument('--draw_map_by_hour', '-b', action='store_true')
    parser.add_argument('text', metavar='T', type=str, nargs='*',
                        help='Text to process')
    args = parser.parse_args()
    for name, execute in args.__dict__.items():
        if name != 'text' and execute:
            globals()[name](' '.join(args.text))

