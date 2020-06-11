def question_block(question_text):
    block = []
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
