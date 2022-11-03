from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login, logout)
from django.utils.timezone import (get_current_timezone, datetime)

from .forms import UploadFileForm
import csv
import xmltodict
import re


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


def check_data(data):
    return all(data) and not re.match(r"^.*((\(.+\))|(\[.+\])).*$", "".join(data))


def handle_uploaded_csv_file(file):
    with open(file.temporary_file_path(), encoding='utf-8') as f:
        data = csv.DictReader(f)
        users_data = [d for d in data if check_data(d.values())]
    return users_data


def handle_uploaded_xml_file(file):
    data = xmltodict.parse(file)
    return [d for d in data['user_list']['user']['users']['user'] if check_data(d.values())]


def get_users_data(file_csv, file_xml):
    csv_data = handle_uploaded_csv_file(file_csv)
    xml_data = handle_uploaded_xml_file(file_xml)
    xml_clean = map(lambda x: {k: v for k, v in x.items() if k not in ['avatar', '@id']}, xml_data)
    result = [{**x_data, **c_data} for x_data in xml_clean
              for c_data in csv_data if f"{x_data['first_name'][0]}.{x_data['last_name']}" == c_data['username']]
    clean_result = map(lambda x: {**x, 'date_joined': datetime.fromtimestamp(
        int(x['date_joined']), tz=get_current_timezone())}, result
                       )
    return list(clean_result)


def add_users_data_to_database(file_csv, file_xml):
    data = get_users_data(file_csv, file_xml)
    users = []
    for d in data:
        try:
            user = User.objects.create_user(**d)
            users.append(user)
        except IntegrityError as e:
            print(f"User {d['username']} is exists. ", e)
            continue

    return users


def upload_files(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            add_users_data_to_database(request.FILES['file_csv'], request.FILES['file_xml'])
            return redirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'load_data.html', {'form': form})
