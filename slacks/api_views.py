import os
import json
import datetime

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from slacks import blocks
from slacks.backends import (
    create_channel_members_dict,
    question_response,
    secret_signing_valid
)
from questions.models import Question
from questions.tasks import respond_notify

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
    response_data = {}
    data = json.loads(request.data['payload'])
    actions = data['actions'][0]
    action_id = actions['action_id']
    channel_id = data['channel']['id']
    if action_id == "urgency_select":
        value_list = actions['selected_option']['value'].split(",")
        question = Question.objects.get(public_id=value_list[0])
        question.status = value_list[1]
        if question.channel_id[0] != 'D':
            question.responses = create_channel_members_dict(question.channel_id, question.created_by)
        question.message_ts = data['container']['message_ts']
        question.save()
        block = blocks.question_block(question.question_text, value_list[1], question.public_id)
        requests.post(
            url=data['response_url'],
            json={
                "channel": channel_id,
                "blocks": block,
                "replace_original": False,
                "delete_original": "true",
                "response_type": "in_channel"
        })
        if question.reminder_time:
            delivery = timezone.now() + question.reminder_time
            respond_notify.apply_async((question.public_id, ), eta=delivery)
    elif action_id == 'cancel_question':
        question = Question.objects.get(public_id=actions['value'])
        requests.post(
            url=data['response_url'],
            json={
                "delete_original": "true",
        })
        question.delete()
    elif action_id == 'question_response_yes':
        question = Question.objects.get(public_id=actions['value'])
        response_text = question_response(data, question, 'yes')
        requests.post(
            url=data['response_url'],
            json={
                "channel": channel_id,
                "text": response_text,
                "replace_original": False,
                "response_type": "ephemeral"
            })
    elif action_id == 'question_response_no':
        question = Question.objects.get(public_id=actions['value'])
        response_text = question_response(data, question, 'no')
        requests.post(
            url=data['response_url'],
            json={
                "channel": channel_id,
                "text": response_text,
                "replace_original": False,
                "response_type": "ephemeral"
            })
    elif action_id == 'new_yes_no_question':
        pass

    return Response(response_data, status=status.HTTP_200_OK, content_type='application/json')


'''
<QueryDict: {'token': ['a5b0ETDdz83wnLwxqYqUqvoH'], 'team_id': ['T0153DP2UNR'], 'team_domain': ['yesnoworkspace'], 'channel_id': ['C014Q2ZS695'], 'channel_name': ['project'], 'user_id': ['U015B0PL1BN'], 'user_name': ['colinjmcfaul'], 'command': ['/question'], 'text': ['Is this working? urgent'], 'response_url': ['https://hooks.slack.com/commands/T0153DP2UNR/1162352845527/fUKP2289tYXkM8Wd7XiMtzUI'], 'trigger_id': ['1200931719072.1173465096773.7593f9f11efcdb628b3d42e70fe88aa4']}>
'''


@csrf_exempt
@api_view(['POST', ])
def question(request):
    if secret_signing_valid(request):
        if request.data['command'] == '/question':
            user_question = "*%s*" % request.data['text']
            channel_id = request.data['channel_id']
            if request.data['text'].strip() == 'help':
                data = {
                    "channel": channel_id,
                    "blocks": blocks.help_command_block()
                }
            elif request.data['text'].strip() == 'feedback':
                data = {
                    "channel": channel_id,
                    "blocks": blocks.feedback_command_block()
                }
            elif len(request.data['text']) > 140:
                data = {
                    "channel": channel_id,
                    "text": "Your question is longer than 140 characters."
                }
            elif "?" not in request.data['text']:
                data = {
                    "channel": channel_id,
                    "text": "We didn't notice a question mark. Are you sure you're asking a quesiton?"
                }
            else:
                question = Question.objects.create(
                    created_by=request.data['user_id'],
                    question_text=user_question,
                    channel_id=channel_id
                )
                data = {
                    "channel": channel_id,
                    "blocks": blocks.confirm_question_create_block(user_question, question.public_id)
                }

        else:
            print(request.data)
            data = {}

        return Response(data, status=status.HTTP_200_OK)
    else:
        try:
            print(request.META['HTTP_X_SLACK_SIGNATURE'])
        except:
            pass
        return Response(status=status.HTTP_403_FORBIDDEN)


@csrf_exempt
@api_view(['POST', 'GET'])
def events(request):
    print(request.POST)
    print(request.META['HTTP_X_SLACK_SIGNATURE'])
    data = {
        'challenge': request.POST['challenge'],
    }

    return Response(data, status=status.HTTP_200_OK)

    '''

if request.data['type'] == 'app_home_opened':
    data = {

    }
else:
    
if request.META['HTTP_X_SLACK_SIGNATURE'] == SLACK_SIGNING_SECRET:
    pass
else:
    return Response(status=status.HTTP_403_FORBIDDEN)
'''