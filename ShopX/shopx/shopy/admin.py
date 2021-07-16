from django.contrib import admin
from .models import Customer,Product,Cart,OrderPlaced

# Register your models here.

@admin.register(Customer)
class CustomerModelsAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'name', 'locality', 'city','zipcode','state']

@admin.register(Product)
class ProductModelsAdmin(admin.ModelAdmin):
    list_display = ['id','title','price','discounted_price','description','brand','category','product_image']

@admin.register(Cart)
class CartModelsAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelsAdmin(admin.ModelAdmin):
    list_display = ['id','user','customer', 'product','quantity', 'ordered_date', 'status']