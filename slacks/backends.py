import os

from slack import WebClient

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
