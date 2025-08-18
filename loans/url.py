from django.urls import path
from. import views

urlpatterns=[
    path("apply_loan/", views.apply_loan, name="apply_loan"),
    path("status/", views.application_status, name="application_status"),
    path("getApplications/", views.fetch_loan_applications, name="fetch_loan_applications"),
]