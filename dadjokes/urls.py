# dadjoke URL Configuration

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
	url(r'^', include('website.urls')),
    url(r'^api/v1/', include('api.urls')),
    url(r'^admin/', admin.site.urls),
]
