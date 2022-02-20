from django.contrib import admin
from .models import Item, Cart, OrderPlaced, PaymentDone

admin.site.register(Item)
admin.site.register(PaymentDone)
@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'product', 'quantity', 'ordered_date', 'status']