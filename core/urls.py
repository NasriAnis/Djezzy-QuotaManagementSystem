from django.urls import path

from . import views

urlpatterns = [
    path("", views.client_index_page, name="client_index_page"),
    path("offers/<slug:offer_slug>/", views.offer_detail_page, name="offer_detail_page")
]