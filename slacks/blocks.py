def question_block(question_text, urgency, question_public_id):

    status = {
        'U': "*Urgent* :rotating_light: - respond in the next 3 hours",
        'N': "*Normal* :timer_clock: - respond in the next 24 hours",
        'W': "*Whenever* :snail: - respond in the next 72 hours"
    }

    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": question_text
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Yes"
                    },
                    "style": "primary",
                    "value": str(question_public_id),
                    "action_id": "question_response_yes"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "No"
                    },
                    "style": "danger",
                    "value": str(question_public_id),
                    "action_id": "question_response_no"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": status[urgency]
                }
            ]
        }
    ]
    return block


def question_response(question):
    value_block = ""
    for user in question.responses:
        user_item = question.responses[user]
        if user_item['answer'] == 'yes':
            value_text = "@%s :white_check_mark:" % user_item['username']
        elif user_item['answer'] == 'no':
            value_text = "@%s :x:" % user_item['username']
        else:
            value_text = "@%s :hourglass_flowing_sand:" % user_item['username']
        value_block = "%s%s\n" % (value_block, value_text)

    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": question.question_text
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": value_block
            }
        }
    ]
    return block


def confirm_question_create_block(question_text, question_public_id):
    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": question_text
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
                            "value": "%s,U" % question_public_id
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Normal: in the next 24 hours"
                            },
                            "value": "%s,N" % question_public_id
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Whenever: in the next 72 hours"
                            },
                            "value": "%s,W" % question_public_id
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
                    "value": question_public_id,
                    "action_id": "cancel_question"
                }
            ]
        }
    ]
    return block


def response_reminder(question):
    status = {
        'U': ":rotating_light: *Urgent* - respond in the next 3 hours",
        'N': ":timer_clock: *Normal* - respond in the next 24 hours",
        'W': ":snail: *Whenever* - respond in the next 72 hours"
    }

    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*You still need to answer this question*"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": question.question_text
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Yes"
                    },
                    "style": "primary",
                    "value": str(question.public_id),
                    "action_id": "question_response_yes"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "No"
                    },
                    "style": "danger",
                    "value": str(question.public_id),
                    "action_id": "question_response_no"
                }
            ]
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": status[question.status]
                }
            ]
        }
    ]
    return block


def help_command_block():

    block = [

    ]

    return block


def feedback_command_block():

    block = [

    ]

    return block


def welcome_block():

    block = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Thanks for using Ouino! To get started, just use the */question* command followed by the question you want to ask. Your question needs to have a question mark in it and needs to be less than 140 characters."
            }
        },
    ]

    return block
