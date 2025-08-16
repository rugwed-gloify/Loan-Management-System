from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.forms.fields import CharField


# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=255,blank=False, null=False)
    last_name = models.CharField(max_length=255,blank=False, null=False)
    phone_no = PositiveIntegerField(max_length=10,blank=False, null=False, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number')],)
    address = CharField(max_length=255,required=True,)
    email = models.EmailField(blank=False,null=False)
    password = models.CharField(max_length=20,blank=False, null=False)
    confirm_password = models.CharField(max_length=20,blank=False, null=False)


