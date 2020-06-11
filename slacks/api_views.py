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

'''
<QueryDict: {'payload': ['{"type":"block_actions","user":{"id":"U015B0PL1BN","username":"colinjmcfaul","name":"colinjmcfaul","team_id":"T0153DP2UNR"},"api_app_id":"A015HDULDKK","token":"a5b0ETDdz83wnLwxqYqUqvoH","container":{"type":"message","message_ts":"1591910755.000100","channel_id":"C014Q2ZS695","is_ephemeral":true},"trigger_id":"1172910493366.1173465096773.621177eb12eabea7aeefee22f64f297e","team":{"id":"T0153DP2UNR","domain":"yesnoworkspace"},"channel":{"id":"C014Q2ZS695","name":"project"},"response_url":"https:\\/\\/hooks.slack.com\\/actions\\/T0153DP2UNR\\/1185822901604\\/7hHKe6obk8Hrm4UjaCA9XrsR","actions":[{"type":"static_select","action_id":"urgency_select","block_id":"quY0","selected_option":{"text":{"type":"plain_text","text":"Urgent: in the next three hours","emoji":true},"value":"U"},"placeholder":{"type":"plain_text","text":"Urgency","emoji":true},"action_ts":"1591910942.744196"}]}']}>
'''


@csrf_exempt
@api_view(['POST', 'GET'])
def interactive_commands(request):

    data = request.data['payload']
    action_id = data['actions']['action_id']
    channel_id = data['channel']['id']
    if action_id == "urgency_select":
        print('yes')
    if action_id == 'cancel_question':
        requests.post(
            url=request.data['response_url'],
            json={
                "delete_original": "true",
            }
        )

    return Response(status=status.HTTP_200_OK)

'''
<QueryDict: {'token': ['a5b0ETDdz83wnLwxqYqUqvoH'], 'team_id': ['T0153DP2UNR'], 'team_domain': ['yesnoworkspace'], 'channel_id': ['C014Q2ZS695'], 'channel_name': ['project'], 'user_id': ['U015B0PL1BN'], 'user_name': ['colinjmcfaul'], 'command': ['/question'], 'text': ['Is this working? urgent'], 'response_url': ['https://hooks.slack.com/commands/T0153DP2UNR/1162352845527/fUKP2289tYXkM8Wd7XiMtzUI'], 'trigger_id': ['1200931719072.1173465096773.7593f9f11efcdb628b3d42e70fe88aa4']}>
'''
@csrf_exempt
@api_view(['POST', ])
def question(request):

    print(request.data)

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
                        "type": "actions",
                        "elements": [
                            {
                                "type": "static_select",
                                "action_id": "urgency_select",
                                "placeholder": {
                                    "type": "plain_text",
                                    "text": "Urgency",
                                },
                                "options": [
                                    {
                                        "text": {
                                            "type": "plain_text",
                                            "text": "Urgent: in the next three hours"
                                        },
                                        "value": "U"
                                    },
                                    {
                                        "text": {
                                            "type": "plain_text",
                                            "text": "Normal: in the next 24 hours"
                                        },
                                        "value": "N"
                                    },
                                    {
                                        "text": {
                                            "type": "plain_text",
                                            "text": "Whenever: in the next 72 hours"
                                        },
                                        "value": "W"
                                    }
                                ]
                            },
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Cancel"
                                },
                                "style": "danger",
                                "value": "cancel",
                                "action_id": "cancel_question"
                            }
                        ]
                    }
                ]
            }
        )
    else:
        print(request.data)

    return Response(status=status.HTTP_200_OK)
