from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.auth import login


def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        profile_picture = request.FILES.get('profile_picture')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Account with this email already exists')
            return render(request, 'Reg & Logins/Register.html')

        user = CustomUser.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        
        if profile_picture:
            user.profile_picture = profile_picture
        
        user.save()
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('register')  

    return render(request, 'Reg & Logins/Register.html')



@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'redirect': '/dashboard_view/'})  
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'})
    return render(request, 'Reg & Logins/Login.html')

@login_required
def dashboard_view(request):
    return render(request, "Dashbords/Dashboard.html", {'user': request.user})