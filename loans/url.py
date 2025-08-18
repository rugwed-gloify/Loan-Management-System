from django.urls import path
from. import views

urlpatterns=[
    path("apply_loan/", views.apply_loan, name="apply_loan"),
    path("status/", views.application_status, name="application_status"),
    path("fetch-loan-status/", views.application_status, name="application_status"),
]