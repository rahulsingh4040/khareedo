from django.contrib import admin
from .models import Product, order, OrderUpdate, Feedback

admin.site.register(Product)
admin.site.register(order)
admin.site.register(OrderUpdate)
admin.site.register(Feedback)