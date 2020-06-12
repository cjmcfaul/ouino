def question_block(question_text, urgency):

    status = {
        'U': ":rotating_light: *Urgent:* respond in the next 3 hours",
        'N': ":timer_clock: *Normal:* respond in the next 24 hours",
        'W': ":snail: *Whenever:* respond in the next 72 hours"
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
                    "value": "yes",
                    "action_id": "question_response_yes"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "No"
                    },
                    "style": "danger",
                    "value": "no",
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


def confirm_question_create_block(question_text):
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
    return block
