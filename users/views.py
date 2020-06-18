from django.shortcuts import render


def support(request):

    return render(request, 'user/support.html', {

    })


def install(request):
    print(request.content)
    return render(request, 'users/install.html', {

    })
