# Django-Authentication
REST APIs based on Django, to signup/signin, signout and resetpassword. Api to list users based on current user group. 

Only connection to PostgreSQL database remains.

**Requirements**
>﻿asgiref==3.2.10
 
>Django==3.1

>django-environ==0.4.5

>django-rest-framework==0.1.0

>django-rest-passwordreset==1.1.0

>djangorestframework==3.11.1

>djangorestframework-simplejwt==4.4.0

>psycopg2==2.8.5

>PyJWT==1.7.1

>pytz==2020.1

>sqlparse==0.3.1

## How to run on your system

### create virtual environment
python -m venv env

## activate virtual environment
.\env\Scripts\activate

## upgrade pip tool
python -m pip install --upgrade pip

## install project dependencies in current virtual environment
pip install django
pip install django-rest-framework
pip install djangorestframework_simplejwt
pip install django-rest-passwordreset
pip install django-environ
pip install psycopg2

## save all project dependencies in requirements.txt
pip freeze > requirements.txt

## start project
django-admin startproject django_auth

## start app in django_auth
python manage.py startapp api

## djangorestframework_simplejwt - this modules needs to be installed
### for JWT authentication, as rest_framework token service
### doesn't work well with requirements.
