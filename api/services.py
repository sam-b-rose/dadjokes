import schedule
import time
from threading import Thread

import praw
import re

import numpy as np
from gensim import corpora
from gensim.models import ldamodel, ldamulticore

from django.conf import settings


def postpone(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()

    return decorator


def on_app_ready():
    schedule_jobs()


@postpone
def schedule_jobs():
    print('Scheduling jobs...')
    get_jokes()
    schedule.every().day.at("10:30").do(get_jokes)

    while True:
        schedule.run_pending()
        time.sleep(1)


def get_jokes():
    my_user_agent = 'ChangeMeClient/0.1 by {username}'.format(username=settings.REDDIT_USERNAME)
    my_client_id = settings.REDDIT_CLIENT_ID
    my_client_secret = settings.REDDIT_CLIENT_SECRET
    my_username = settings.REDDIT_USERNAME
    my_password = settings.REDDIT_PASSWORD

    print('Getting dad jokes...')
    reddit = praw.Reddit(user_agent=my_user_agent,
                         client_id=my_client_id,
                         client_secret=my_client_secret,
                         username=my_username,
                         password=my_password)

    after = ''
    r_dadjokes = reddit.subreddit('dadjokes')

    for i in range(20):
        params = {'after': after}
        hot_jokes = r_dadjokes.hot(params=params)
        after = process_jokes(hot_jokes, after)

    print('Updated jokes in database: {}'.format(time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime())))


def process_jokes(raw_jokes, after):
    from api.models import Jokes

    jokes = [clean_joke(joke) for joke in raw_jokes]
    for joke, is_last in last_joke(jokes):
        if is_last:
            after = joke['name']
        if not Jokes.objects.filter(reddit_id=joke['reddit_id']).exists():
            Jokes(**joke).save()
    return after


def clean_joke(joke):
    return {
        'reddit_id': joke.id,
        'setup': joke.title,
        'punchline': joke.selftext,
        'url': joke.url,
        'score': joke.score,
        'name': joke.name
    }


def last_joke(seq):
    seq = iter(seq)
    a = next(seq)
    for b in seq:
        yield a, False
        a = b
    yield a, True

# ------------ WIP: Recommendation Learning ------------- # 


def fit_data():
    from api.models import Jokes

    jokes = Jokes.objects.all()
    words_tokens = ['{} {}'.format(
        re.sub('[^0-9a-zA-Z]+', '*', joke.setup.encode('ascii', 'replace')),
        re.sub('[^0-9a-zA-Z]+', '*', joke.punchline.encode('ascii', 'replace'))
        ).split('*') for joke in jokes]

    # print(words_tokens)
    words_dictionary = corpora.Dictionary(words_tokens)
    words_dictionary.filter_extremes(no_above=0.02)
    # print(words_dictionary)

    words_corpus = [words_dictionary.doc2bow(tokens) for tokens in words_tokens]
    # print(words_corpus[0:10])

    words_lda = ldamulticore.LdaModel(corpus=words_corpus, num_topics=10)
    print('LDA initialization complete')
    words_lda.save('big_booty_hoes.txt')

    for i in range(10):
        terms = words_lda.get_topic_terms(i, topn=5)
        print('[Word Topic %d]' % i)
        for (key, prob) in terms:
            print('  %s, %lf' % (words_dictionary.get(key=key), prob))


def get_related(joke):
    pass
