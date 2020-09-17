from django.contrib import admin
from .models import Contests,Problems,CFUsers

admin.site.register(Contests)
admin.site.register(CFUsers)
# admin.site.register(Resources)
admin.site.register(Problems)
# Register your models here.
