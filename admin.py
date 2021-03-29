from django.contrib import admin
from django.contrib.admin import register
from .models import Contests,Problems,CFUsers

admin.site.register(Contests)

@register(CFUsers)
class CFUsersAdmin(admin.ModelAdmin):
    list_display = ('handle','page_visits','last_seen')

# admin.site.register(CFUsers)
# admin.site.register(Resources)
admin.site.register(Problems)
# Register your models here.
