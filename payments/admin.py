from django.contrib import admin
from .models import Item, Order, OrderItem, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'price', 'currency']


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'tax', 'discount', 'currency']
    inlines = [OrderItemInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'percent_off']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'percentage']
