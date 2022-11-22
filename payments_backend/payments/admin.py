from django.contrib import admin
from .models import Item, Order, OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price']


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    inlines = [OrderItemInline]
