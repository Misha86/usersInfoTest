import csv
import xmltodict
import re
from django.utils.timezone import (get_current_timezone, datetime)
from django.contrib.auth.models import User
from django.db import IntegrityError


class DataUploadService:
    def __init__(self, file_csv, file_xml):
        self._file_csv = file_csv
        self._file_xml = file_xml

    def handle_uploaded_csv_file(self):
        with open(self._file_csv.temporary_file_path(), encoding='utf-8') as f:
            data = csv.DictReader(f)
            users_data = [d for d in data if self.check_data(d.values())]
        return users_data

    def handle_uploaded_xml_file(self):
        data = xmltodict.parse(self._file_xml)
        return [d for d in data['user_list']['user']['users']['user'] if self.check_data(d.values())]

    @staticmethod
    def check_data(data):
        return all(data) and not re.match(r"^.*((\(.+\))|(\[.+\])).*$", "".join(data))

    def get_users_data(self):
        csv_data = self.handle_uploaded_csv_file()
        xml_clean = self.clean_xml_data()
        result = [{**x_data, **c_data} for x_data in xml_clean
                  for c_data in csv_data if f"{x_data['first_name'][0]}.{x_data['last_name']}" == c_data['username']]
        return self.clean_result_data(result)

    def clean_xml_data(self):
        xml_data = self.handle_uploaded_xml_file()
        return map(lambda x: {k: v for k, v in x.items() if k not in ['avatar', '@id']}, xml_data)

    def clean_result_data(self, result):
        return list(map(lambda x: {**x, 'date_joined': datetime.fromtimestamp(
            int(x['date_joined']), tz=get_current_timezone())}, result))

    def add_users_data_to_database(self):
        data = self.get_users_data()
        users = []
        for d in data:
            try:
                user = User.objects.create_user(**d)
                users.append(user)
            except IntegrityError as e:
                print(f"User {d['username']} is exists. ", e)
                continue

        return users


