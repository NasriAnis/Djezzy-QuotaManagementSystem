from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse


def commercials_index_page(request):
    if request.user.is_authenticated:
        return redirect('commercials_dashboard_page')
    return redirect('commercials_login')

def client_logout(request):
    logout(request)
    return redirect('commercials_login')

def commercials_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('commercials_dashboard_page')
        else:
            return render(request, 'interns/commercials_login_page.html', {'error': 'Invalid credentials'})
    return render(request, 'interns/commercials_login_page.html')

@login_required(login_url='commercial_login')
def commercials_dashboard_page(request):
    return HttpResponse("Hello dashboard")