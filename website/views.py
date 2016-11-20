import requests
from django.conf import settings
from django.shortcuts import render

SLACK_AUTH_URL = 'https://slack.com/api/oauth.access'
REDIRECT_URI = 'https://dadjokes.samrose3.com/auth'
STATE = 'dadjokes'


def index(request):
    return render(request, 'index.html')


def auth(request):
    if request.GET.get('code') and request.GET.get('state') == STATE:
        r = requests.get(SLACK_AUTH_URL, {
            'client_id': settings.SLACK_CLIENT_ID,
            'client_secret': settings.SLACK_CLIENT_SECRET,
            'code': request.GET.get('code'),
            'redirect_uri': REDIRECT_URI
        })
    return render(request, 'auth.html')
