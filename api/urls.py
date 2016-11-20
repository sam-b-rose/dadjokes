from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^jokes/$', views.JokesList.as_view()),
    url(r'^joke/(?P<pk>[0-9]+)/$', views.JokeDetail.as_view()),
    url(r'^dadjokes/$', views.DadJokes.as_view()),
    url(r'^feedback/$', views.Feedback.as_view()),
]
