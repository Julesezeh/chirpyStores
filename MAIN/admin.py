from django.contrib import admin
from .models import Product,BasePopup, ProductCategory, ShoeBrand, SizeAvailable
# Register your models here.

admin.site.register(Product)
admin.site.register(BasePopup)
admin.site.register(ProductCategory)
admin.site.register(ShoeBrand)
admin.site.register(SizeAvailable)
