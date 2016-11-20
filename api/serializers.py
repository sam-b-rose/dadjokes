from rest_framework import serializers
from api.models import Jokes


class JokesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jokes
        fields = ('id', 'reddit_id', 'setup', 'punchline', 'url', 'rating', 'votes', 'score', 'name', 'created')
