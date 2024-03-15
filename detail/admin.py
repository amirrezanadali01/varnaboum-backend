from django.contrib import admin
from .models import Banner, UpdateVersionModel

# Register your models here.


class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'action')
    list_filter = ('action',)
    search_fields = ('title',)


admin.site.register(Banner, BannerAdmin)
admin.site.register(UpdateVersionModel)
