from django.contrib import admin
from .models import Product, order, OrderUpdate

admin.site.register(Product)
admin.site.register(order)
admin.site.register(OrderUpdate)