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
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="loans")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.loan_type} Loan - {self.user.email} ({self.status})"






class Repayment(models.Model):
    due_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateField(auto_now_add=True)
    loan_id = models.ForeignKey(Loan,on_delete=models.CASCADE)
    installment_number = models.PositiveIntegerField(null=True, blank=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)

class Repayments(models.Model):

    due_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateField(null=True,blank=True)
    loan = models.ForeignKey(Loan,on_delete=models.CASCADE)
    installment_number = models.PositiveIntegerField(null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True)
