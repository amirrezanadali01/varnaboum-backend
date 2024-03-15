from django.contrib import admin
from .models import *

# Register your models here.


class InfoUserAdmin(admin.ModelAdmin):
    readonly_fields = ('user_id',)
    list_display = ('user', 'name', 'category', 'Confirmation', 'top')
    list_filter = ('Confirmation', 'city', 'category')
    search_fields = ('user__username', 'name',)


class InfoUserManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('category',)
    search_fields = ('name', 'user__username')


class QuestionProfileAdminl(admin.ModelAdmin):
    list_display = ('question', 'is_required', 'category')
    list_filter = ('is_required', 'category')
    search_fields = ('question',)


class AnswerProfileAdminl(admin.ModelAdmin):
    list_display = ('user', 'question')
    search_fields = ('user',)


class ShopImageAdmin(admin.ModelAdmin):
    search_fields = ('user',)


class ProductsAnotherAdminl(admin.ModelAdmin):
    list_display = ('name', 'infouser', 'created')
    list_filter = ('created',)
    search_fields = ('name', 'infouser__name')


class ProductsImageAnotherAdminl(admin.ModelAdmin):

    search_fields = ('products__name',)


admin.site.site_header = "وارنابوم"
admin.site.register(ContactUsModel)
admin.site.register(InfoUserModel, InfoUserAdmin)
admin.site.register(QuestionProfileModel, QuestionProfileAdminl)
admin.site.register(AnswerProfileModel, AnswerProfileAdminl)
admin.site.register(Shop_Image, ShopImageAdmin)
admin.site.register(CityModel)
admin.site.register(VerifyCodeModel)
admin.site.register(ProductsAnotherModel, ProductsAnotherAdminl)
admin.site.register(ProductsImageAnotherModel, ProductsImageAnotherAdminl)
admin.site.register(ManagerStore, InfoUserManagerAdmin)
