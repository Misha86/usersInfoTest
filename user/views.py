from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout)


def hello(request):
    return render(request, 'index.html')


def sing_in(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'login.html', {'error': "Inputted data is incorrect!"})


def logout_view(request):
    logout(request)
    return redirect('/')