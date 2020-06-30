from django.contrib import admin
from .models import Contests,Problems,Invitees

@admin.register(Contests)
class ContestsAdmin(admin.ModelAdmin):
    list_display = ('contid','conttype','duration','difficulty')

@admin.register(Problems)
class ContestsAdmin(admin.ModelAdmin):
    list_display = ('contestId','index','name','userssolved')

admin.site.register(Invitees)
# admin.site.register(Resources)