from django.contrib import admin
from .models import *
# Register your models here.


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'top')
    list_filter = ('city',)
    search_fields = ('name',)


class UserOfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'office', 'user')
    list_filter = ('office',)
    search_fields = ('name', 'office__name', 'user__username')


admin.site.register(OfficeModel, OfficeAdmin)
admin.site.register(UserOfficeModel, UserOfficeAdmin)
