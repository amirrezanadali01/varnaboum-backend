from django.contrib import admin
from .models import ImageEstateProductsModel, ProductsEstateModel, TypeEstateModel

# Register your models here.
admin.site.register(TypeEstateModel)
admin.site.register(ProductsEstateModel)
admin.site.register(ImageEstateProductsModel)
