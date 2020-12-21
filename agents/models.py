from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
#from phonenumber_field.modelfields import PhoneNumberField
User = get_user_model

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone = models.IntegerField()
    region = models.CharField(max_length=64)
    billing_address = models.CharField(max_length=400)
    delivery_address = models.CharField(max_length=400)
    vat_number = models.IntegerField()
    pub_date = models.DateTimeField('date published')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="agent", blank=True)

    def __str__(self):
        return f"{self.id} | {self.name} | {self.email} | {self.phone} | {self.region} | {self.billing_address} | {self.delivery_address} | {self.vat_number} | {self.pub_date} | {self.created_by}"



