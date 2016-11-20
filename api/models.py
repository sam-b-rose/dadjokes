from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

@python_2_unicode_compatible
class Jokes(models.Model):
    reddit_id = models.CharField(max_length=10, blank=False)
    setup = models.CharField(max_length=500, blank=False)
    punchline = models.TextField(blank=False)
    url = models.URLField(max_length=500, blank=False, default='https://reddit.com/r/dadjokes')
    name = models.CharField(max_length=10)
    score = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    votes = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.setup
