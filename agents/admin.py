from django.contrib import admin
from .models import Customer
from import_export.formats import base_formats
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        fields = ("id", "name", "email", "phone", "region", "billing_address", "delivery_address", "vat_number", "pub_date", "created_by")


# Register your models here.
class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ("id", "name", "email", "phone", "region", "billing_address", "delivery_address", "vat_number", "pub_date", "created_by")
    resource_class = CustomerResource
    list_editable = ("name", "email")
    list_filter = ("region", "created_by")
    

admin.site.register(Customer, CustomerAdmin)  