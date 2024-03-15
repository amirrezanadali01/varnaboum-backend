from django.contrib import admin
from .models import *
# Register your models here.


class NewsAdminl(admin.ModelAdmin):
    list_display = ('titr', 'category', 'office', 'city')
    list_filter = ('category', 'city')
    search_fields = ('titr',)


class TopNewsAdminl(admin.ModelAdmin):

    search_fields = ('office__name',)


class NewsPeopleAdminl(admin.ModelAdmin):
    list_display = ('titr', 'city', 'user', 'name')
    list_filter = ('city',)
    search_fields = ('titr', 'user__username')


admin.site.register(NewsModel, NewsAdminl)
admin.site.register(CategoryNewsModel)
admin.site.register(TopNewsModel, TopNewsAdminl)
admin.site.register(NewsPeopleModel, NewsPeopleAdminl)
