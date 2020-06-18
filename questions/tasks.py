from __future__ import absolute_import, unicode_literals

from yes_no.celery import app
from questions.models import Question
from slacks.backends import response_reminder


@app.task
def respond_notify(question_id):
    question = Question.objects.get(public_id=question_id)
    if question.responses:
        for user in question.responses:
            user_info = question.responses[user]
            if not user_info['answer']:
                response_reminder(user, question)

    return "Done"
