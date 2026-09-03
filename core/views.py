from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Offer, OfferPlan, OfferQuota, OfferCategory
from clients.models import Store, StoreOfferTransaction

# def client_index_page(request):
#     offers = Offer.objects.filter(is_active=True)
#     categories = OfferCategory.objects.all()

#     # search / filter query logic here

#     context = {
#         'offers': offers,
#         'categories': categories,
#     }
#     return render(request, 'core/client_index.html', context)

# def offer_detail_page(request, offer_slug):
#     offer = get_object_or_404(Offer, slug=offer_slug, is_active=True)
#     offer_plans = offer.plans.all()

#     context = {
#         'offer': offer,
#         'offer_plans': offer_plans,
#     }
#     return render(request,"core/offer_details_page.html", context)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Offer, OfferPlan, OfferQuota, OfferCategory
from clients.models import Store, StoreOfferTransaction

def client_index_page(request):
    offers = Offer.objects.filter(is_active=True)
    categories = OfferCategory.objects.all()

    # search / filter query logic here

    context = {
        'offers': offers,
        'categories': categories,
    }
    return render(request, 'core/client_index.html', context)

def offer_detail_page(request, offer_slug):
    offer = get_object_or_404(Offer, slug=offer_slug, is_active=True)
    offer_plans = offer.plans.all()

    user_stores = []
    selected_store = None
    quota_info = None

    if request.user.is_authenticated and hasattr(request.user, 'client_profile'):
        user_stores = request.user.client_profile.locations.all()
        
        selected_store_id = request.GET.get('store_id')
        if selected_store_id:
            selected_store = user_stores.filter(id=selected_store_id).first()
        else:
            selected_store = user_stores.first()

        if selected_store:
            formatted_wilaya_code = str(selected_store.wilaya).zfill(2)
            quota_info = OfferQuota.objects.filter(
                offer=offer,
                wilaya_code=formatted_wilaya_code
            ).first()

    # Form handling for custom quantity purchases
    if request.method == 'POST':
        if not request.user.is_authenticated or not selected_store:
            messages.error(request, "You must select a valid store to place an order.")
            return redirect('offer_detail_page', offer_slug=offer.slug)

        plan_id = request.POST.get('plan_id')
        plan = get_object_or_404(OfferPlan, id=plan_id, offer=offer)

        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                raise ValueError
        except ValueError:
            messages.error(request, "Please enter a valid quantity of at least 1.")
            return redirect('offer_detail_page', offer_slug=offer.slug)

        with transaction.atomic():
            formatted_wilaya_code = str(selected_store.wilaya).zfill(2)
            
            # Lock the quota row to prevent race conditions during checkout
            current_quota = OfferQuota.objects.select_for_update().filter(
                offer=offer,
                wilaya_code=formatted_wilaya_code
            ).first()

            if current_quota and current_quota.is_available(quantity):
                # 1. Register or update transaction under the selected store
                store_tx, created = StoreOfferTransaction.objects.get_or_create(
                    store=selected_store,
                    plan=plan,
                    defaults={'quantity_bought': quantity}
                )
                if not created:
                    store_tx.quantity_bought += quantity
                    store_tx.save()

                # 2. Increase allocated quota in core DB (decreases remaining_quota)
                current_quota.allocated_quota += quantity
                current_quota.save()

                messages.success(
                    request, 
                    f"Successfully purchased {quantity}x '{plan.label}' for {selected_store.name}!"
                )
                return redirect('offer_detail_page', offer_slug=offer.slug)
            else:
                available = current_quota.remaining_quota if current_quota else 0
                messages.error(
                    request, 
                    f"Order failed. Requested {quantity} units, but only {available} remaining for your Wilaya."
                )

    context = {
        'offer': offer,
        'offer_plans': offer_plans,
        'user_stores': user_stores,
        'selected_store': selected_store,
        'quota_info': quota_info,
    }
    return render(request, 'core/offer_details_page.html', context)