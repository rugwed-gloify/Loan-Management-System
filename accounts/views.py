from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
# Create your views here.
from django.contrib import messages
from .models import User
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
        return redirect("dashboard")  # redirect to login page

    return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:

            user = User.objects.get(email = email)
            print("-------------------------***************",user.email)
            if check_password(password,user.password):
                messages.success(request, f"Welcome {user.first_name}!")
                return render(request,'dashboard.html',{"user": user})
            else:

                messages.error(request, "Invalid password")
                return render(request, "login.html")
        except User.DoesNotExist:
            messages.error(request,"Invalid email or password")

    return render(request,'login.html')


def dashboard(request):
    return render(request,'dashboard.html')