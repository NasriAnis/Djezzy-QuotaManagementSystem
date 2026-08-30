from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientSignupForm
from .models import Client

def client_signup(request):
    if request.method == 'POST':
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
            )
            Client.objects.create(user=user, phone=data.get('phone', ''))
            login(request, user)
            return redirect('client_account_page', username=user.username)
    else:
        form = ClientSignupForm()
    return render(request, 'clients/client_signup_page.html', {'form': form})


def client_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('client_account_page', username=user.username)
        else:
            return render(request, 'clients/client_login_page.html', {'error': 'Invalid credentials'})
    return render(request, 'clients/client_login_page.html')


def client_logout(request):
    logout(request)
    return redirect('client_login')


@login_required(login_url='client_login')
def client_account_page(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('client_account_page', username=request.user.username)
    client = user.client_profile
    return render(request, 'clients/client_account_page.html', {'client': client})