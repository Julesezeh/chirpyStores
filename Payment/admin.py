from django.contrib import admin
from . models import Payment, Order, OrderItem, BillingInformation

# Register your models here.

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BillingInformation)