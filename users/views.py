from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import mail_admins

from slacks.backends import get_oauth

from users.forms import (
    FeedbackForm,
)


def support(request):

    return render(request, 'users/support.html', {

    })


def install(request):
    code = request.GET.get('code', None)
    get_oauth(code)
    return render(request, 'users/install.html', {

    })


def more_info(request):

    return render(request, 'more_info.html', {
        'footer': True,
    })


def feedback(request):

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            email_2 = form.cleaned_data['email_2']
            if email_2 != '':
                return HttpResponse(status=403)
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email_address']
            user_message = form.cleaned_data['message']
            subject = "New Feedback Form Submission - %s" % (full_name)
            email_text = "New Feedback Form Submission \r\n Name: %s \r\n Email: %s \r\n Message: %s" % (
                full_name, email, user_message)
            email_html = '<h2 style="color:#597DC6"><b>New Contact Us Form Submission</b></h2><p><b>Name:</b> %s</p><p><b>Email:</b> %s</p><p><b>Message:</b>\r\n%s</p>' % (
                full_name, email, user_message)
            mail_admins(
                subject,
                email_text,
                'Admin Notifications <admin-notifications@ouino.app>',
                html_message=email_html
            )
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {
        'form': form
    })
