import json
from api.models import Jokes
from api.serializers import JokesSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class JokesList(APIView):
    """
    List all jokes, or create a new joke.
    """
    def get(self, request, format=None):
        jokes = Jokes.objects.all()
        serializer = JokesSerializer(jokes, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = JokesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JokeDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_joke(self, pk):
        try:
            return Jokes.objects.get(pk=pk)
        except Jokes.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        joke = self.get_joke(pk)
        serializer = JokesSerializer(joke)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        joke = self.get_joke(pk)
        serializer = JokesSerializer(joke, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        joke = self.get_joke(pk)
        joke.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DadJokes(APIView):
    def get(self, request, format=None):
        joke = Jokes.objects.order_by('?').first()
        return Response(self.format_joke(joke), status=status.HTTP_200_OK)

    def post(self, request, format=None):
        joke = Jokes.objects.order_by('?').first()
        return Response(self.format_joke(joke), status=status.HTTP_200_OK)

    def format_joke(self, joke):
        return {
            'response_type': "in_channel",
            'text': joke.setup,
            'attachments': [{
                'callback_id': joke.id,
                'text': '{punchline} - <{url}|source>'.format(punchline=joke.punchline, url=joke.url),
                'fallback': 'Sorry, we are having trouble telling jokes at the moment.',
                'actions': [{
                    'name': 'upvote',
                    'text': 'Good one!',
                    'type': 'button',
                    'value': 'upvote'
                }, {
                    'name': 'downvote',
                    'text': 'Not funny.',
                    'type': 'button',
                    'value': 'downvote'
                }]
            }]
        }


class Feedback(APIView):
    def post(self, request, format=None):
        feedback = json.loads(request.data.get('payload'))
        action = feedback.get('actions')[0]
        # Save feedback
        joke = Jokes.objects.get(pk=feedback['callback_id'])
        joke.rating += 1 if action['value'] == 'upvote' else -1
        joke.votes += 1;
        joke.save()
        return Response(self.format_feedback(feedback), status=status.HTTP_200_OK)

    def format_feedback(self, feedback):
        orig_msg = feedback.get('original_message')
        orig_msg['attachments'][0]['actions'] = []
        orig_msg['attachments'][0]['footer'] = "Thanks for the feedback!"
        return orig_msg
