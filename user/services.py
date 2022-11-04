"""Module for all project services."""
import csv
import re

import requests
import xmltodict
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import IntegrityError
from django.utils import timezone
from django.utils.timezone import get_current_timezone

from .models import CustomUser


class DataUploadService:
    """Class for data uploading services."""

    def __init__(self, file_csv, file_xml):
        self._file_csv = file_csv
        self._file_xml = file_xml

    def handle_uploaded_csv_file(self):
        """Upload data from .cvs files."""
        with open(self._file_csv.temporary_file_path(), encoding='utf-8') as f:
            data = csv.DictReader(f)
            users_data = [d for d in data if self.check_data(d.values())]
        return users_data

    def handle_uploaded_xml_file(self):
        """Upload data from .xml files."""
        data = xmltodict.parse(self._file_xml)
        return [d for d in data['user_list']['user']
                ['users']['user'] if self.check_data(d.values())]

    @staticmethod
    def check_data(data):
        """Check data for empty values or for including [] or () in the values."""
        return all(data) and not re.match(r"^.*((\(.+\))|(\[.+\])).*$", "".join(data))

    def get_users_data(self):
        """Get users data from .csv and .xml files."""
        csv_data = self.handle_uploaded_csv_file()
        xml_clean = self.clean_xml_data()
        result = [{**x_data, **c_data} for x_data in xml_clean
                  for c_data in csv_data if f"{x_data['first_name'][0]}.{x_data['last_name']}" == c_data['username']]
        return self.change_date_joined_value(result)

    def clean_xml_data(self):
        """Remove '@id' item from users data."""
        xml_data = self.handle_uploaded_xml_file()
        return map(lambda x: {k: v for k, v in x.items() if k not in ['@id']}, xml_data)

    def change_date_joined_value(self, result):
        """Change date_joined value to DateTime type."""
        return list(map(lambda x: {**x, 'date_joined':
                                   timezone.datetime.fromtimestamp(int(x['date_joined']), tz=get_current_timezone())}, result))

    def add_users_data_to_database(self):
        """Create new users and add them to the database."""
        data = self.get_users_data()
        users = []
        for d in data:
            try:
                user = CustomUser.objects.create_user(**d)
                self.upload_avatar(d, user)
                users.append(user)
            except IntegrityError as e:
                print(f"User {d['username']} is exists. ", e)
                continue
        return users

    def upload_avatar(self, user_data, user):
        """Upload image using URL and save it to the media storage.."""
        avatar_url = user_data.get("avatar")
        avatar_image_ending = re.split('[/.]', avatar_url)[-1]
        image_content = requests.get(avatar_url).content
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(image_content)
        img_temp.flush()
        user.avatar.save(f"{user.id}.{avatar_image_ending}", File(img_temp))
