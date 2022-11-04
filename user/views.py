from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import UploadFileForm
from .models import CustomUser
from .services import DataUploadService


def users_list(request):
    context = {}
    if request.user.is_superuser:
        users = CustomUser.objects.exclude(is_superuser=True)
        context["users_list"] = users
    return render(request, 'index.html', context=context)


def sing_in(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, 'login.html', {'error': "Inputted data is incorrect!"}, status=403)
    login(request, user)
    return redirect('/')


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
