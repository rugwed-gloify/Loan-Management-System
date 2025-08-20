from django.urls import path
from. import views

urlpatterns=[
    path("apply_loan/", views.apply_loan, name="apply_loan"),
    path("status/", views.application_status, name="application_status"),
    path("getApplications/", views.fetch_loan_applications, name="fetch_loan_applications"),
    path("getUserStatistics/", views.user_application_summary, name="user_application_summary"),
    path("getApprovedApplication/", views.get_approved_applications, name="get_approved_applications"),
    path("repayments/<int:loan_id>/", views.get_repayments, name="get_repayments"),
    path("getInstallmentById/<int:installment_number>/<int:loanId>/", views.get_emi_status, name="get_emi_status"),
    path("payEMI/<int:installment_number>/<int:loanId>", views.pay_emi, name="pay_emi"),

]