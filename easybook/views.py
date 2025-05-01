import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from .utils import send_user_to_inventory
from rest_framework.authtoken.models import Token



def verify_payment_view(request):
    email = request.GET.get("email")
    password = request.GET.get("password")
    full_name = request.GET.get("full_name")
    telephone = request.GET.get('telephone')
    reference = request.GET.get("ref")

    if not all([email, password, full_name, telephone, reference]):
        return render(request, "payment_failed.html", {"message": "Missing required parameters"})

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    verify_url = f"https://api.paystack.co/transaction/verify/{reference}"
    response = requests.get(verify_url, headers=headers)
    data = response.json()

    if data.get("data", {}).get("status") == "success":
        # Split full name safely
        if full_name:
            first_name, *rest = full_name.split(" ")
            last_name = " ".join(rest)
        else:
            first_name = ""
            last_name = ""

        user, created = User.objects.get_or_create(username=email, email=email)
        if created:
            user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            # Optional: Send to inventory backend
            # send_user_to_inventory(email, full_name, reference)
        login(request, user)
        return redirect("dashboard")
    else:
        return render(request, "payment_failed.html", {"message": "Payment failed"})

def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if User.objects.filter(username=email).exists():
            messages.error(request, "User with this email already exists.")
            return render(request, "signup.html", {"PAYSTACK_PUBLIC_KEY": settings.PAYSTACK_PUBLIC_KEY})
        user = User.objects.create_user(username=email, email=email, password=password)
        login(request, user)
        return redirect("dashboard")
    return render(request, "signup.html", {"PAYSTACK_PUBLIC_KEY": settings.PAYSTACK_PUBLIC_KEY})

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "login.html")

def dashboard_view(request):
    return render(request, "dashboard.html")
from django.shortcuts import render

def admin_dashboard_view(request):
    return render(request, "admin_dashboard.html")

def index(request):
    return render(request, 'landing.html')

def payment_success_view(request):
    # You must confirm the payment is actually successful first via Paystack verification

    if request.user.is_authenticated:
        user = request.user  # or get by email or ID if unauthenticated
        token, created = Token.objects.get_or_create(user=user)

        # Optionally: send token to user or just return it as part of JSON response
        headers = {
            'Authorization': f'Token {token.key}'
        }
        inventory_api_url = 'https://inventory.yourdomain.com/api/inventory/'

        response = requests.get(inventory_api_url, headers=headers)

        if response.status_code == 200:
            # Inventory data or access granted
            inventory_data = response.json()
            return JsonResponse({
                'message': 'Payment successful. Access granted!',
                'inventory': inventory_data
            })
        else:
            return JsonResponse({'error': 'Access denied to inventory'}, status=403)
    else:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

