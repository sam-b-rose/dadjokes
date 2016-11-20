from rest_framework import serializers
from api.models import Joke


class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ('id', 'reddit_id', 'setup', 'punchline', 'url', 'rating', 'votes', 'score', 'name', 'created')
