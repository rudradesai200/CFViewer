import os

SECRET_KEY = 'django-insecure-12h#20b048+%wwcmz)d3+6x=r9ftkjy2#iz#(jc62#*mf@qfiv'
DEBUG = True
ALLOWED_HOSTS = ['*']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Uncomment the below lines and add details about 
# production database if needed
# and remove the default database

# if not DEBUG:
    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'some_django_engine',
    #         'NAME': 'basic_db',
    #         'USER': 'admin',
    #         'PASSWORD': 'something',
    #         'HOST': 'something@domain.com',
    #         'PORT': 'xxxx',    
    #     }
    # }

    

# This is just an example 
# add your own values
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'something@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'

CORS_ALLOWED_ORIGINS = [
    "https://codeforces.com",
]