from django.contrib import admin

from store.models import Product, Category, TotalArchive, ProductCategories

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(TotalArchive)
admin.site.register(ProductCategories)
