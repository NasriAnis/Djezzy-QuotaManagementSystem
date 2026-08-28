from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Offer, OfferCategory, OfferPlan

def client_index_page(request):
    offers = Offer.objects.filter(is_active=True)
    categories = OfferCategory.objects.all()

    # search / filter query logic here

    context = {
        'offers': offers,
        'categories': categories,
    }
    return render(request, 'client_index.html', context)

def offer_detail_page(request, offer_slug):
    offer = get_object_or_404(Offer, slug=offer_slug, is_active=True)
    offer_plans = offer.plans.all()

    context = {
        'offer': offer,
        'offer_plans': offer_plans,
    }
    return render(request,"offer_details_page.html", context)