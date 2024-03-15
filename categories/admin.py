from django.contrib import admin
from .models import CategoryModel, RegionCityModel, SubCategoryModel, SubtitleModel, VillageModel

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'top')
    search_fields = ('name',)


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'name')
    list_filter = ('category',)
    search_fields = ('name',)


class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name',)


class RegionCityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name',)


class SubtitleAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(CategoryModel, CategoryAdmin)
admin.site.register(SubCategoryModel, SubCategoryAdmin)
admin.site.register(SubtitleModel, SubtitleAdmin)


# UPDATEEEEEEEEEEEEEEE
admin.site.register(VillageModel, VillageAdmin)
admin.site.register(RegionCityModel, RegionCityAdmin)
