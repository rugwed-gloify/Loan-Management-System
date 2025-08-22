from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields import PositiveIntegerField
from django.forms.fields import CharField


# Create your models here.

class User(models.Model):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("CUSTOMER", "Customer"),
    )


    first_name = models.CharField(max_length=255,blank=False, null=False)
    last_name = models.CharField(max_length=255,blank=False, null=False)
    phone_no = models.CharField(blank=False,max_length=10, null=False, validators=[RegexValidator(r'^\d{10}$', 'Enter a valid 10-digit phone number')],)
    address = models.CharField(max_length=255,blank=False,null = False)
    email = models.EmailField(unique=True,blank=False,null=False)
    password = models.CharField(max_length=255,blank=False, null=False)
    confirm_password = models.CharField(max_length=255,blank=False, null=False)
    date_joined = models.DateTimeField(auto_now_add = True)
    isActive = models.PositiveIntegerField(default=0)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="CUSTOMER")



