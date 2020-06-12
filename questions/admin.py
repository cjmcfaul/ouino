from django.contrib import admin
from questions.models import Question


class QuestionAdmin(admin.ModelAdmin):

    model = Question


admin.site.register(Question, QuestionAdmin)
