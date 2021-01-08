from django.contrib import admin

# Register your models here.
from order.models import ShopCart, Order, OrderProduct
from import_export.formats import base_formats
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class OrderResource(resources.ModelResource):
    class Meta:
        model = Order
        fields = ('code', 'user', 'customer','total','status', 'create_at')

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product','user','customer','quantity','price','amount', 'vattotal', 'total' ]
    list_filter = ['user']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('user', 'product','price','quantity','total_amount')
    can_delete = False
    extra = 0



class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['code', 'user', 'customer','total','status', 'create_at']
    resource_class = OrderResource
    list_filter = ['status', 'create_at', 'user']
    readonly_fields = ('user','customer','ip','total', 'code')
    can_delete = False
    inlines = [OrderProductline]

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['order', 'user', 'customer', 'product','price','quantity','total_amount']
    list_filter = ['user']

admin.site.register(ShopCart,ShopCartAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)