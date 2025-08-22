from django.contrib import admin

from loans.models import Loan, Repayments
from django.utils import timezone

from loans.views import create_repayment_schedule


# Register your models here.

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ("user","loan_type","loan_amount","status","created_at","approved_at")
    list_filter = ("status", "loan_type", "created_at")
    actions = ["approve_loans","reject_loans"]
    def approve_loans(self, request, queryset):
        for loan in queryset:
            loan.status = "Approved"
            loan.approved_at = timezone.now()
            loan.save()
            # Call repayment schedule generator here
            create_repayment_schedule(loan)

        self.message_user(request, f"{queryset.count()} loan(s) marked as Approved and repayment schedule created.")


    def reject_loans(self, request, queryset):
        updated = queryset.update(status="Rejected", approved_at=None)
        self.message_user(request, f"{updated} loan(s) marked as Rejected.")

    approve_loans.short_description = "Approve selected loans"
    reject_loans.short_description = "Reject selected loans"


@admin.register(Repayments)
class RepaymentHistory(admin.ModelAdmin):
    list_display = ("user","loan","due_date","installment_number","emi_amount","is_paid","paid_at")
    list_filter = ("user","is_paid","due_date")