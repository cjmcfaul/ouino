import os

from slack import WebClient

from slacks import blocks

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

slack_client = WebClient(SLACK_BOT_TOKEN)


def create_channel_members_dict(channel_id, created_by):

    member_dict = dict()

    response = slack_client.conversations_members(channel=channel_id)
    for member in response['members']:
        if member != created_by:
            member_dict[member] = {
                'answer': None,
            }

    return member_dict


def question_response(data, question, answer):
    new_message = False
    print(data)
    print(question.responeses)
    if question.created_by != data['user']['id']:
        if question.responses is None:
            question.responses = {
                data['user']['id']: {
                    'answer': None,
                }
            }
            new_message = True
        elif data['user']['id'] in question.responses:
            print(question.responses[data['user']['id']]['answer'])
            if question.responses[data['user']['id']]['answer'] is None:
                question.responses[data['user']['id']]['answer'] = answer
                new_message = True

        if new_message:
            if not question.response_message_ts:
                response = slack_client.chat_postMessage(
                    channel=question.created_by,
                    blocks=blocks.question_response(answer, question.question_text, data['user']['username']),
                    reply_broadcast=True
                )
                question.response_message_ts = response['ts']
            else:
                slack_client.chat_update(
                    channel=question.channel_id,
                    ts=question.response_message_ts,
                    attachments=blocks.question_response(answer, question.question_text, data['user']['username']),
                )
            question.save()
            return 'Thanks for responding!'
        else:
            return "You've already responded to this question"
    else:
        return "You can't answer your own question"
