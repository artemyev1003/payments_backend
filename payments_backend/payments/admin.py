from django.contrib import admin
from .models import Item, Order, OrderItem


admin_models = [Item, Order, OrderItem]
admin.site.register(admin_models)
