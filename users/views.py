from django.shortcuts import render


def support(request):

    return render(request, 'user/support.html', {

    })


def install(request):
    print(request.body)
    return render(request, 'users/install.html', {

    })
