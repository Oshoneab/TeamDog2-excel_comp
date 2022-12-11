from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate,login,logout

def Login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            if not username or not password:
                messages.success(request, 'Both Username and Password are required.')
                return redirect('/login/')
            user_obj = User.objects.filter(username = username).first()
            if user_obj is None:
                messages.success(request, 'User not found.')
                return redirect('/login/')

            user = authenticate(username = username, password = password)

            if user is None:
                messages.success(request, 'Wrong Password.')
                return redirect('/login/')

            login(request, user)
            return redirect('/')

    except Exception as e:
        print(e)
    return render(request, 'signUp.html')

def Register(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            try:
                if User.objects.filter(username = username).first():
                    messages.success(request, 'Username is taken.')
                    return redirect('/register/')
                if User.objects.filter(email = email).first():
                    messages.success(request, 'Email is taken.')
                    return redirect('/register/')

                user_obj = User(username = username, email = email)
                user_obj.set_password(password)
                user_obj.save()

                profile_obj = Profile.objects.create(user = user_obj)
                profile_obj.save()
                return redirect('/login/')
            
            except Exception as e:
                print(e)
            
            return render(request, 'signUp.html')
    

