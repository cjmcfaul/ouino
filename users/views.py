from django.shortcuts import render

from slacks.backends import get_oauth


def support(request):

    return render(request, 'user/support.html', {

    })


# https://www.ouino.app/install/?code=1173465096773.1177687522231.a84c10fd2ec530db7b0699b2fef17e0ed13411b49ad6783dff1a24901363d7e6&state=
def install(request):
    code = request.GET.get('code', None)
    get_oauth(code)
    return render(request, 'users/install.html', {

    })
