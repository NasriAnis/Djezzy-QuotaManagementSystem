from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ClientSignupForm, StoreForm
from .models import Client, Commune
from django.http import JsonResponse
from clients.backends import EmailBackend

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
            login(request, user, backend='clients.backends.EmailBackend')
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

def get_communes(request):
    wilaya_code = request.GET.get('wilaya') or request.GET.get('wilaya_code')
    if not wilaya_code:
        return JsonResponse([], safe=False)

    padded_code = str(wilaya_code).zfill(2)

    communes = Commune.objects.filter(wilaya_code=padded_code).order_by('name').values('id', 'name')
    return JsonResponse(list(communes), safe=False)

@login_required(login_url='client_login')
def client_dashboard_page(request, username):
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect('client_dashboard_page', username=request.user.username)
    client = user.client_profile
    stores = client.locations.all().order_by('-created_at')

    if request.method == 'POST':
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            store.client = client
            store.save()
            return redirect('client_dashboard_page', username=username)
    else:
        form = StoreForm()

    return render(request, 'clients/client_dashboard_page.html', {
        'client': client,
        'stores': stores,
        'form': form,
    })

# @login_required(login_url='client_login')
# def client_account_page(request, username):
#     user = get_object_or_404(User, username=username)
#     if request.user != user:
#         return redirect('client_account_page', username=request.user.username)
#     client = user.client_profile
#     return render(request, 'clients/client_account_page.html', {'client': client})

# @login_required(login_url='client_login')
# def client_stores_page(request, username):
#     user = get_object_or_404(User, username=username)
#     if request.user != user:
#         return redirect('client_stores_page', username=request.user.username)

#     client = user.client_profile
#     stores = client.locations.all().order_by('-created_at')

#     if request.method == 'POST':
#         form = StoreForm(request.POST)
#         if form.is_valid():
#             store = form.save(commit=False)
#             store.client = client
#             store.save()
#             return redirect('client_stores_page', username=username)
#     else:
#         form = StoreForm()

#     return render(request, 'clients/client_stores_page.html', {
#         'client': client,
#         'stores': stores,
#         'form': form,
#     })
