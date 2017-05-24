import schedule
import time
from threading import Thread

import praw

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
