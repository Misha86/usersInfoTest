from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout)
from .models import CustomUser

from .forms import UploadFileForm
from .services import DataUploadService


def users_list(request):
    context = {}
    if request.user.is_superuser:
        users = CustomUser.objects.exclude(is_superuser=True)
        context.update({"users_list": users})
    return render(request, 'index.html', context=context)


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
        return render(request, 'login.html', {'error': "Inputted data is incorrect!"}, status=403)


def logout_view(request):
    logout(request)
    return redirect('/')


def upload_files(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_service = DataUploadService(request.FILES['file_csv'], request.FILES['file_xml'])
            upload_service.add_users_data_to_database()
            return redirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'load_data.html', {'form': form})
