def question_block(question_text, urgency, question_public_id):

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
        value_block = "%s\n" % value_text

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
