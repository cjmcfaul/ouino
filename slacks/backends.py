import os
import requests
import json
import hmac
import hashlib

from slack import WebClient

from slacks import blocks
from slacks.models import Team
from users.models import CustomUser

SLACK_CLIENT_ID = os.environ["SLACK_CLIENT_ID"]
SLACK_CLIENT_SECRET = os.environ["SLACK_CLIENT_SECRET"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]


def get_slack_client(team_id):

    team = Team.objects.get(slack_id=team_id)
    slack_client = WebClient(team.bot_access_token)
    return slack_client


def create_channel_members_dict(question):

    member_dict = dict()

    bot_token = question.user.team.bot_access_token

    slack_client = WebClient(bot_token)

    response = slack_client.conversations_members(channel=question.channel_id)
    for member in response['members']:
        if member != question.created_by:
            url = "https://slack.com/api/users.info?token=%s&user=%s" %(bot_token, member)
            user_info = requests.get(
                url=url
            )
            user_info = json.loads(user_info.text)
            if user_info:
                if not user_info['user']['is_bot']:
                    member_dict[member] = {
                        'answer': None,
                        'username': user_info['user']['name']
                    }

    return member_dict


def create_users_from_team(team):

    slack_client = WebClient(team.bot_access_token)
    response = slack_client.users_list()
    for user in response['members']:
        if not user['is_bot']:
            if 'email' in user['profile']:
                email = user['profile']['email']
            else:
                email = None

            if len(user['profile']['phone']) > 10:
                phone = user['profile']['phone']
            elif len(user['profile']['phone']) == 10:
                phone = "+1%s" % user['profile']['phone']
            else:
                phone = None

            CustomUser.objects.create_user(
                username=user['profile']['display_name'],
                slack_id=user['id'],
                team=team,
                full_name=user['profile']['real_name_normalized'],
                title=user['profile']['title'],
                email=email,
                phone=phone
            )


def question_response(data, question, answer):
    new_message = False
    if question.created_by != data['user']['id']:
        if not question.responses:
            question.responses = {
                data['user']['id']: {
                    'answer': answer,
                    'username': data['user']['username']
                }
            }
            new_message = True
        elif data['user']['id'] in question.responses:
            if question.responses[data['user']['id']]['answer'] is None:
                question.responses[data['user']['id']]['answer'] = answer
                new_message = True
        else:
            question.responses[data['user']['id']] = {
                'answer': answer,
                'username': data['user']['username']
            }
            new_message = True

        if new_message:
            try:
                slack_client = get_slack_client(data['team']['id'])
            except:
                return print(data)
            if not question.response_message_ts:
                response = slack_client.chat_postMessage(
                    channel=question.created_by,
                    blocks=blocks.question_response(question),
                    reply_broadcast=True
                )
                question.response_message_ts = response['ts']
            else:
                slack_client.chat_update(
                    channel=question.channel_id,
                    ts=question.response_message_ts,
                    attachments=blocks.question_response(question),
                )
            question.save()
            return 'Thanks for responding!'
        else:
            return "You've already responded to this question"
    else:
        return "You can't answer your own question"


def response_reminder(channel_id, question):
    slack_client = WebClient(question.user.team.bot_access_token)
    slack_client.chat_postMessage(
        channel=channel_id,
        blocks=blocks.response_reminder(question)
    )


def secret_signing_valid(request):
    slack_secret = request.META['HTTP_X_SLACK_SIGNATURE']
    timestamp = request.META['HTTP_X_SLACK_REQUEST_TIMESTAMP']
    sig_basestring = 'v0:' + timestamp + ':' + request.body.decode("utf-8")
    my_signature = 'v0=' + hmac.new(
        str.encode(SLACK_SIGNING_SECRET),
        sig_basestring.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    if my_signature == slack_secret:
        return True
    else:
        return False


def get_oauth(code):
    slack_client = WebClient()
    response = slack_client.oauth_v2_access(
        client_id=SLACK_CLIENT_ID,
        client_secret=SLACK_CLIENT_SECRET,
        code=code
    )
    team, new = Team.objects.get_or_create(
        slack_id=response['team']['id']
    )
    if new:
        team.name = response['team']['name']
        team.bot_access_token = response['access_token']
        team.bot_slack_id = response['bot_user_id']
        team.save()

    try:
        CustomUser.objects.get(
            slack_id=response['authed_user']['id']
        )
    except:
        CustomUser.objects.create_user(
            username=response['authed_user']['id'],
            slack_id=response['authed_user']['id'],
            slack_access_token=response['authed_user']['access_token'],
            team=team,
        )

    return 'success'
