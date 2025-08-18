from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from .models import Loan
# Create your views here.
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation

@csrf_exempt
def apply_loan(request):
    if request.method == "POST":
        loan_type = request.POST.get("loan_type")
        print("______________________________88888888")
        loan_amount = request.POST.get("loan_amount")
        print("loan amount",loan_amount)

        tenure = request.POST.get("tenure")
        print("Tenure",tenure)

        purpose = request.POST.get("purpose")


        interest_rate = request.POST.get("interest_rate")
        print("INterest rate",interest_rate)

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
        Loan.objects.create(
            user=user,
            loan_type=loan_type,
            loan_amount=loan_amount,
            tenure=tenure,
            purpose=purpose,
            interest_rate=interest_rate,
        )
        return JsonResponse({"message": "Your application was submitted successfully"}, status=200)

    return JsonResponse({"error": "Invalid request method"}, status=405)


     # show form page

def application_status(request):
    loans = Loan.objects.filter(user=request.user)
    return render(request, "loans/application_status.html", {"loans": loans})

