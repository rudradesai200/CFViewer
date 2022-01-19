from django.contrib import admin
from django.contrib.admin import register
from .models import Contests,Problems

admin.site.register(Contests)
admin.site.register(Problems)
