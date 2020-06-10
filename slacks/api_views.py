from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import requests

@csrf_exempt
@api_view(['POST', ])
def interactive_commands(request):
    print(request.data)
    return Response(status=status.HTTP_200_OK)

'''
<QueryDict: {'token': ['a5b0ETDdz83wnLwxqYqUqvoH'], 'team_id': ['T0153DP2UNR'], 'team_domain': ['yesnoworkspace'], 'channel_id': ['C014Q2ZS695'], 'channel_name': ['project'], 'user_id': ['U015B0PL1BN'], 'user_name': ['colinjmcfaul'], 'command': ['/question'], 'text': ['Is this working? urgent'], 'response_url': ['https://hooks.slack.com/commands/T0153DP2UNR/1162352845527/fUKP2289tYXkM8Wd7XiMtzUI'], 'trigger_id': ['1200931719072.1173465096773.7593f9f11efcdb628b3d42e70fe88aa4']}>
'''
@csrf_exempt
@api_view(['POST', ])
def question(request):

    print(request.data['team_id'])
    print(request.data['response_url'])

    channel_id = request.data['channel_id']

    message_data = {
        'channel': channel_id,
        'text': 'testing to see if slash command works',
    }

    data = requests.post(url=request.data['response_url'], data=message_data)

    print(data)

    return Response(status=status.HTTP_200_OK)