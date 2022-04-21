from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


def login(request):
    match request.method:
        case 'POST':
            username, password = request.POST.get('username').lower(), request.POST.get('password')
            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, 'User not found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            user = authenticate(request, username=username, password=password)

            # if we find user
            if user is not None:
                auth_login(request, user)
                return redirect('home.index')
            else:
                # if we don't find user
                messages.error(request, 'Username or Password does not exist')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        case default:
            # if user is logged in
            if request.user.is_authenticated:
                messages.info(request, 'Already logged in')
                return redirect('home.index')
            else:
                # if not logged in
                return render(request, 'authentication/login.html')


def register(request):
    match request.method:
        case 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                auth_login(request, user)
                messages.success(request, 'User has been created, and you are logged in')
                return redirect('home.index')
            else:
                messages.error(request, 'Please enter valid data')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        case default:
            # rendering registration page on other methods
            context = {'form': UserCreationForm()}
            return render(request, 'authentication/register.html', context)


def logout(request):
    match request.method:
        case 'GET':
            print('Logged out')
            auth_logout(request)
            return redirect('home.index')
        case default:
            print('Invalid logout request with method', request.method)
            return redirect('home.index')
