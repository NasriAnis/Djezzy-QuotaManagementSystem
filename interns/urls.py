from django.urls import path
from . import views

urlpatterns = [
    path('', views.commercials_index_page, name='commercials_index_page'),
    path('login/', views.commercials_login, name='commercials_login'),
    path('dashboard/', views.commercials_dashboard_page, name='commercials_dashboard_page'),
]