from django.db import models
from django.db.models.fields import CharField


# Create your models here.

class Loan(models.Model):

    PERSONAL_LOAN = ' PL'
    HOME_LOAN = 'HL'
    VEHICLE_LOAN = 'VL'
    EDUCATION_LOAN = 'EL'

    LOAN_CHOICES = [
        (PERSONAL_LOAN,'Personal Loan'),
        (HOME_LOAN,'Home Loan'),
        (VEHICLE_LOAN,'Vehicle Loan'),
        (EDUCATION_LOAN,'Education Loan')

    ]

    loan_type = CharField(choices=LOAN_CHOICES)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, default=50000.00)
    tenure = models.PositiveIntegerField(help_text="In months")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual %")
    purpose = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)

    # Personal Loan, Home Loan, Vehicle Loan, Education Loan

