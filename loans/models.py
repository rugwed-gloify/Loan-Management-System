from tkinter.constants import CASCADE
from django.db import models
from django.db.models.fields import CharField
from django.conf import settings
from accounts.models import User
# Create your models here.

class Loan(models.Model):

    PERSONAL_LOAN = 'PL'
    HOME_LOAN = 'HL'
    VEHICLE_LOAN = 'VL'
    EDUCATION_LOAN = 'EL'

    LOAN_CHOICES = [
        (PERSONAL_LOAN,'Personal Loan'),
        (HOME_LOAN,'Home Loan'),
        (VEHICLE_LOAN,'Vehicle Loan'),
        (EDUCATION_LOAN,'Education Loan')

    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    loan_type = CharField(choices=LOAN_CHOICES,max_length=2)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.PositiveIntegerField(help_text="In months")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual %")
    purpose = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="loans")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.loan_type} Loan - {self.user.username} ({self.status})"


