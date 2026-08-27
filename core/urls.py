from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_page, name="index_page"),
    path("offers/<slug:offer_slug>/", views.offer_detail_page, name="offer_detail_page")
]