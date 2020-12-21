from django.contrib import admin
from .models import Customer

# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "region", "billing_address", "delivery_address", "vat_number", "pub_date", "created_by")
    list_editable = ("name", "email")
    

admin.site.register(Customer, CustomerAdmin)  