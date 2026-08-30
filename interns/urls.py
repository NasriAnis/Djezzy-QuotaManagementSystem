from django.urls import path
from . import views

urlpatterns = [
    path('', views.commercial_index_page, name='commercial_index_page'),
    path('dashboard/', views.commercial_dashboard_page, name='commercial_dashboard_page'),
]