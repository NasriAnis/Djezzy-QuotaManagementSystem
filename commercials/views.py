from django.shortcuts import render
from django.http import HttpResponse

def commercial_dashboard_page(request):
    return HttpResponse("Hello dashboard")

def commercial_index_page(request):
    return HttpResponse("Hello index")