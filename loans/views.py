from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from accounts.models import User
from .models import Loan
# Create your views here.
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from django.utils import timezone
from datetime import timedelta
import math
from django.template.loader import render_to_string
from notifications import utils
from .models import Repayments

@csrf_exempt
def apply_loan(request):
    if request.method == "POST":
        loan_type = request.POST.get("loan_type")
        loan_amount = request.POST.get("loan_amount")
        tenure = request.POST.get("tenure")
        purpose = request.POST.get("purpose")
        interest_rate = request.POST.get("interest_rate")

        if not loan_type or not loan_amount or not tenure or not purpose or not interest_rate:
            messages.error(request, "All fields are required ******")
             # reload form with error

        user_id = request.session.get("user_id")
        if not user_id:
            return redirect("login")  # or show an error message

        user = get_object_or_404(User, id=user_id)

        try:
            loan_amount = Decimal(loan_amount)
            interest_rate = Decimal(interest_rate)
            tenure = int(tenure)
        except (InvalidOperation, ValueError):
            return JsonResponse({"error": "Invalid numeric input"}, status=400)

        loan = Loan.objects.create(
            user=user,
            loan_type=loan_type,
            loan_amount=loan_amount,
            tenure=tenure,
            purpose=purpose,
            interest_rate=interest_rate,
        )


        utils.send_loan_confirmation_email(user,loan)

        return JsonResponse({"message": "Your application was submitted successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


     # show form page

def application_status(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, "loans/application_status.html", {"loans": loans})

@csrf_exempt
def fetch_loan_applications(request):
    if request.method == "GET":
        print("Inside the fetch ")
        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({"error": "Unauthorized"}, status=401)

        loans = Loan.objects.filter(user_id=user_id).values(
            "id", "loan_type", "loan_amount", "tenure", "interest_rate", "status", "created_at"
        )

        return JsonResponse(list(loans), safe=False, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def format_amount(amount):
    if amount >= 1_00_00_000:  # 1 Crore = 1,00,00,000
        return f"{amount/1_00_00_000:.2f} Cr"
    elif amount >= 1_00_000:   # 1 Lakh = 1,00,000
        return f"{amount/1_00_000:.2f} Lakh"
    elif amount >= 1_000:      # 1 Thousand = 1,000
        return f"{amount/1_000:.2f} K"
    else:
        return str(amount)


@csrf_exempt
def user_application_summary(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({"error": "Not logged in"}, status=401)

        # user = User.objects.get(id=user_id)

        total_applications = Loan.objects.filter(user_id=user_id).count()
        approved = Loan.objects.filter(user_id=user_id, status="Approved").count()
        pending = Loan.objects.filter(user_id=user_id, status="Pending").count()
        rejected = Loan.objects.filter(user_id=user_id, status="Rejected").count()

        total_approved_amount = (
                Loan.objects.filter(user_id=user_id, status="Approved")
                .aggregate(total=Sum("loan_amount"))["total"] or 0
        )

        return JsonResponse({
            "total_applications": total_applications,
            "approved": approved,
            "pending": pending,
            "rejected": rejected,
            "total_approved_amount": format_amount(total_approved_amount),
        })

def get_approved_applications(request):
    if(request.method == 'GET'):
        if not request.session.get('user_id'):
            redirect('login')

        user_id = request.session.get('user_id')
        approvedApplications = Loan.objects.filter(user_id = user_id,status = "Approved")
        data = list(approvedApplications.values())
        return JsonResponse(data,safe = False,status=200)
    return JsonResponse("Incorrect request",status=405)

@csrf_exempt
def create_repayment_schedule(loan):
    print("Inside the create ",loan)
    principal = float(loan.loan_amount)
    rate = float(loan.interest_rate)
    tenure = loan.tenure

    # Monthly EMI calculation
    monthly_rate = rate / (12 * 100)
    emi = (principal * monthly_rate * (1 + monthly_rate)**tenure) / ((1 + monthly_rate)**tenure - 1)

    outstanding = principal
    start_date = loan.approved_at.date()

    for i in range(1, tenure + 1):
        interest_component = outstanding * monthly_rate
        principal_component = emi - interest_component
        outstanding -= principal_component
        print("Inside the for loop")
        Repayments.objects.create(
            loan=loan,
            user=loan.user,
            installment_number=i,
            due_date=start_date + timedelta(days=30 * i),
            emi_amount=emi,
            is_paid=False
        )

@csrf_exempt
def get_repayments(request, loan_id):
    print("Inside the get_repayments",loan_id)
    loan = Loan.objects.get(id=loan_id)
    print(loan.id)
    create_repayment_schedule(loan)
    repayments = Repayments.objects.filter(id=loan_id).order_by("installment_number")
    print("repayments -----",repayments)
    data = [
        {
            "emiNumber": r.installment_number,
            "dueDate": r.due_date.isoformat(),
            "emiAmount": float(r.emi_amount),
            "isPaid": r.is_paid,
            "status": "Paid" if r.is_paid else ("Overdue" if r.due_date < timezone.now().date() else "Due"),
        }
        for r in repayments
    ]
    print(data)
    return JsonResponse(data, safe=False)

@csrf_exempt
def pay_emi(request, installment_number,loanId):
    if request.method == "POST":
        print("#############################3")
        user_id = request.session.get("user_id")
        repayment = Repayments.objects.get(installment_number=installment_number,loan_id = loanId,user_id = user_id)
        repayment.is_paid = True
        repayment.paid_at = timezone.now()
        repayment.save()
        return JsonResponse({"message": "EMI Paid Successfully!"},status=200)

@csrf_exempt
def get_emi_status(request,installment_number,loanId):
    if request.method == 'GET':
        print("------------------------------------------------------------------")
        user_id = request.session.get("user_id")
        print("******************",user_id)
        try:
            installment = Repayments.objects.get(installment_number=installment_number,loan_id = loanId,user_id = user_id)
            print(installment)
            return JsonResponse(model_to_dict(installment), status=200)
        except Repayments.DoesNotExist:
            return JsonResponse({"error": "Installment not found"}, status=404)
