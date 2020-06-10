import os
import json

from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from slack import WebClient
import requests

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(SLACK_BOT_TOKEN)


@csrf_exempt
@api_view(['POST', 'GET'])
def interactive_commands(request):
    print(request.GET)
    print(request.body)
    return Response(status=status.HTTP_200_OK)

'''
<QueryDict: {'token': ['a5b0ETDdz83wnLwxqYqUqvoH'], 'team_id': ['T0153DP2UNR'], 'team_domain': ['yesnoworkspace'], 'channel_id': ['C014Q2ZS695'], 'channel_name': ['project'], 'user_id': ['U015B0PL1BN'], 'user_name': ['colinjmcfaul'], 'command': ['/question'], 'text': ['Is this working? urgent'], 'response_url': ['https://hooks.slack.com/commands/T0153DP2UNR/1162352845527/fUKP2289tYXkM8Wd7XiMtzUI'], 'trigger_id': ['1200931719072.1173465096773.7593f9f11efcdb628b3d42e70fe88aa4']}>
'''
@csrf_exempt
@api_view(['POST', ])
def question(request):

    if request.data['command'] == '/question':
        user_question = "*Question:* %s" % request.data['text']
        requests.post(
            url=request.data['response_url'],
            json={
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": user_question
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "When do you need a response?"
                        },
                        "accessory": {
                            "type": "static_select",
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select an item",
                            },
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Urgent: in the next 3 hours",
                                    },
                                    "value": "U"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Normal: in the next 24 hours",
                                    },
                                    "value": "N"
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "Whenever: in the next 72 hours",
                                    },
                                    "value": "W"
                                }
                            ]
                        }
                    }
                ]
            }
        )
    else:
        print(request.data)

    return Response(status=status.HTTP_200_OK)
