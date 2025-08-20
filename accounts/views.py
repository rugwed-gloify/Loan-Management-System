from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import User
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from loans.models import Loan
from django.contrib.auth import authenticate, login as auth_login

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        phone_no = request.POST.get("phone_no")
        address = request.POST.get("address")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")


        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")


        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "register.html")

        # Save user
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_no=phone_no,
            address=address,
            email=email,
            password=make_password(password)  # store hashed password
        )
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect("dashboard")

    return render(request, "register.html")

def login(request):
    if request.session.get('access_token'):
        return redirect('dashboard')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:

            user = User.objects.get(email = email)

            if check_password(password,user.password):

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                request.session['user_id'] = user.id

                messages.success(request, f"Welcome {user.first_name}!")
                return render(request,'dashboard.html',{"user": user})
            else:

                messages.error(request, "Invalid password")
                return render(request, "login.html")
        except User.DoesNotExist:
            messages.error(request,"Invalid email or password")

    return render(request,'login.html')



@csrf_exempt
def dashboard(request):
    user_id = request.session.get('user_id') 
    if not user_id:
        return redirect('login')
    user = User.objects.get(id=user_id)
    return render(request, 'dashboard.html', {"user": user})

@csrf_exempt
def logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')



