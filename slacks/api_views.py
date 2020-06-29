import json

from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from slacks import blocks
from slacks.backends import (
    create_channel_members_dict,
    question_response,
    secret_signing_valid,
    get_slack_client,
    user_change_event
)
from questions.models import Question
from questions.tasks import respond_notify
from users.models import CustomUser

import requests

'''
<QueryDict: {'payload': ['{"type":"block_actions","user":{"id":"U015B0PL1BN","username":"colinjmcfaul","name":"colinjmcfaul","team_id":"T0153DP2UNR"},"api_app_id":"A015HDULDKK","token":"a5b0ETDdz83wnLwxqYqUqvoH","container":{"type":"message","message_ts":"1591910755.000100","channel_id":"C014Q2ZS695","is_ephemeral":true},"trigger_id":"1172910493366.1173465096773.621177eb12eabea7aeefee22f64f297e","team":{"id":"T0153DP2UNR","domain":"yesnoworkspace"},"channel":{"id":"C014Q2ZS695","name":"project"},"response_url":"https:\\/\\/hooks.slack.com\\/actions\\/T0153DP2UNR\\/1185822901604\\/7hHKe6obk8Hrm4UjaCA9XrsR","actions":[{"type":"static_select","action_id":"urgency_select","block_id":"quY0","selected_option":{"text":{"type":"plain_text","text":"Urgent: in the next three hours","emoji":true},"value":"U"},"placeholder":{"type":"plain_text","text":"Urgency","emoji":true},"action_ts":"1591910942.744196"}]}']}>
'''


@csrf_exempt
@api_view(['POST', 'GET'])
def interactive_commands(request):
    if secret_signing_valid(request):
        response_data = {}
        data = json.loads(request.data['payload'])
        actions = data['actions'][0]
        action_id = actions['action_id']
        channel_id = data['channel']['id']
        if action_id == "urgency_select":
            '''
            {'type': 'block_actions', 'user': {'id': 'U015B0PL1BN', 'username': 'colinjmcfaul', 'name': 'colinjmcfaul', 'team_id': 'T0153DP2UNR'}, 'api_app_id': 'A015HDULDKK', 'token': 'a5b0ETDdz83wnLwxqYqUqvoH', 'container': {'type': 'message', 'message_ts': '1593097112.000100', 'channel_id': 'D0154QU02EN', 'is_ephemeral': True}, 'trigger_id': '1212068098484.1173465096773.4213e8fd6dfa36e534813f3efc63f8d5', 'team': {'id': 'T0153DP2UNR', 'domain': 'yesnoworkspace'}, 'channel': {'id': 'D0154QU02EN', 'name': 'directmessage'}, 'response_url': 'https://hooks.slack.com/actions/T0153DP2UNR/1191145409591/aszu5mE8OcHUzuBDoxBJTffZ', 'actions': [{'type': 'static_select', 'action_id': 'urgency_select', 'block_id': 'Vyu', 'selected_option': {'text': {'type': 'plain_text', 'text': 'Urgent: in the next three hours', 'emoji': True}, 'value': '1b09fc77-670f-4759-a668-4aefc5a4c1ad,U'}, 'placeholder': {'type': 'plain_text', 'text': 'Urgency', 'emoji': True}, 'action_ts': '1593097120.098005'}]}
            '''
            value_list = actions['selected_option']['value'].split(",")
            question = Question.objects.get(public_id=value_list[0])
            question.status = value_list[1]
            if question.channel_id[0] != 'D':
                question.responses = create_channel_members_dict(question)
            question.message_ts = data['container']['message_ts']
            question.save()
            block = blocks.question_block(question, value_list[1])
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
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


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
                user = CustomUser.objects.get(slack_id=request.data['user_id'])
                question = Question.objects.create(
                    created_by=request.data['user_id'],
                    question_text=user_question,
                    channel_id=channel_id,
                    user=user
                )
                data = {
                    "channel": channel_id,
                    "blocks": blocks.confirm_question_create_block(question)
                }

        else:
            print(request.data)
            data = {}

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)


'''
{'token': 'a5b0ETDdz83wnLwxqYqUqvoH', 'team_id': 'T0153DP2UNR', 'api_app_id': 'A015HDULDKK', 'event': {'type': 'app_home_opened', 'user': 'U015B0PL1BN', 'channel': 'D014YSJK370', 'tab': 'messages', 'event_ts': '1592588029.082025'}, 'type': 'event_callback', 'event_id': 'Ev015RD8AMRR', 'event_time': 1592588029}
'''
@csrf_exempt
@api_view(['POST', 'GET'])
def events(request):
    if secret_signing_valid(request):
        if request.data['event']['type'] == 'app_home_opened':
            user, new = CustomUser.objects.get_or_create(slack_id=request.data['event']['user'])
            if not user.onboarding_complete:
                slack_client = get_slack_client(request.data['team_id'])
                slack_client.chat_postMessage(
                    channel=request.data['event']['channel'],
                    blocks=blocks.welcome_block(username=user.username)
                )
                user.onboarding_complete = True
                user.save()

        elif request.data['event']['type'] == 'user_change':
            result = user_change_event(request.data)
            if isinstance(result, str):
                print(result)

        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)
