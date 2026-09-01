from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.client_signup, name='client_signup'),
    path('login/', views.client_login, name='client_login'),
    path('logout/', views.client_logout, name='client_logout'),
    path('<str:username>/', views.client_dashboard_page, name='client_dashboard_page'),
    # path('<str:username>/', views.client_account_page, name='client_account_page'),
    # path('<str:username>/stores/', views.client_stores_page, name='client_stores_page'),
    path('ajax/communes/', views.get_communes, name='get_communes'),
]