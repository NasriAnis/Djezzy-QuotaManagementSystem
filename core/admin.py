from django.contrib import admin

from .models import OfferCategory, Offer, OfferPlan

admin.site.register(OfferCategory)
admin.site.register(Offer)
admin.site.register(OfferPlan)