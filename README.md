# UsersInfoTest project

---
Content

- [Installation](#Installation)
  - [Clone](#Clone)
  - [Required to install](#Required-to-install)
  - [Environment](#Environment)
  - [How to run local](#How-to-run-local)
  - [Setup](#Setup)
- [Tests](#Tests)
- [Usage](#Usage)


----

## Installation

### Clone or Download

- Clone this repo to your local machine using

```
git clone https://github.com/Misha86/usersInfoTest.git
```

  or download the project archive: <https://github.com/Misha86/usersInfoTest/archive/refs/heads/main.zip>

<a name="footnote">*</a> - to run the project you need an `.env` file in root folder

### Required to install

- [![Python](https://docs.python.org/3.9/_static/py.svg)](https://www.python.org/downloads/release/python-3912/) 3.9.12
- Project reqirements:

```
pip install -r /requirements.txt
```

### Environment

- Add the environment variables file (.env) to the project folder.
It must contain the following settings:

```
SECRET_KEY = '😊YOUR_SECRET_KEY😊'
DEBUG = False
ALLOWED_HOSTS = *
```

### How to run local

- Start the terminal.
- Go to the directory "your way to the project" /usersInfoTest
- Run the following commands

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```


### Setup

- Create a superuser using the terminal:

```
python manage.py createsuperuser
```

----

## Tests

- Run project tests:

```
python manage.py test
```

----


# Usage

- After start server open browser

```
you will see start page.
```

- Login as superuser
- For load data from files push left top green button
- In form choose files .csv and .xml
- Push 'Upload files' 
- You will be redirected to the home page
- Table with users info will be there

----


