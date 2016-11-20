from __future__ import unicode_literals

from django.apps import AppConfig
from api.services import on_app_ready


class ApiAppConfig(AppConfig):
    name = 'api'
    verbose_name = "Dad Jokes API"

    def ready(self):
        on_app_ready()
