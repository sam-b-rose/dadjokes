from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^privacy', views.privacy, name='privacy'),
    url(r'^support', views.support, name='support'),
    url(r'^auth$', views.auth, name='auth'),
]
