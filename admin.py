from django.contrib import admin
from .models import Contests,Problems,Invitees

admin.site.register(Contests)
admin.site.register(Invitees)
# admin.site.register(Resources)
admin.site.register(Problems)
# Register your models here.
