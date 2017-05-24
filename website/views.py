import requests
from django.conf import settings
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.template.loader import get_template
from forms import ContactForm

SLACK_AUTH_URL = 'https://slack.com/api/oauth.access'
REDIRECT_URI = 'https://dadjokes.samrose3.com/auth'
STATE = 'dadjokes'


def index(request):
    return render(request, 'index.html')

def privacy(request):
    return render(request, 'privacy.html')

def support(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            subject = request.POST.get('subject', '')
            email = request.POST.get('email', '')
            message = request.POST.get('message', '')

            template = get_template('support_template.txt')
            context = {
                'subject': subject,
                'email': email,
                'message': message,
            }
            email_content = template.render(context)

            email = EmailMessage(
                "Support request from /dadjokes",
                email_content,
                "/dadjokes" +'',
                ['samrose3@gmail.com'],
                headers = {'Reply-To': email }
            )
            email.send()
            return redirect('support')

    return render(request, 'support.html', {
        'form': form_class,
    })

def auth(request):
    if request.GET.get('code') and request.GET.get('state') == STATE:
        r = requests.get(SLACK_AUTH_URL, {
            'client_id': settings.SLACK_CLIENT_ID,
            'client_secret': settings.SLACK_CLIENT_SECRET,
            'code': request.GET.get('code'),
            'redirect_uri': REDIRECT_URI
        })
    return render(request, 'auth.html')
