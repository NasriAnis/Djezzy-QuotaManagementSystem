from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.contrib import messages

from core.models import Offer, OfferPlan, OfferQuota, WILAYA_CHOICES
from clients.models import Client, Store, StoreOfferTransaction


def commercials_index_page(request):
    if request.user.is_authenticated:
        return redirect('commercials_dashboard_page')
    return redirect('commercials_login')


def commercials_logout(request):
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


@login_required(login_url='commercials_login')
def commercials_dashboard_page(request):
    revenue_expr = ExpressionWrapper(
        F('quantity_bought') * F('plan__price_da'),
        output_field=DecimalField(max_digits=14, decimal_places=2)
    )
    total_revenue = StoreOfferTransaction.objects.aggregate(
        total=Sum(revenue_expr)
    )['total'] or 0

    context = {
        'offers_count': Offer.objects.count(),
        'clients_count': Client.objects.count(),
        'stores_count': Store.objects.count(),
        'total_revenue': total_revenue,
        'recent_stores': Store.objects.select_related('client__user').order_by('-created_at')[:5],
    }
    return render(request, 'interns/commercials_dashboard_page.html', context)


@login_required(login_url='commercials_login')
def commercials_offers_page(request):
    offers = Offer.objects.select_related('category').prefetch_related('plans').all()
    return render(request, 'interns/commercials_offers_page.html', {'offers': offers})


@login_required(login_url='commercials_login')
def commercials_offer_edit_page(request, slug):
    offer = get_object_or_404(Offer, slug=slug)
    can_edit = hasattr(request.user, 'commercial_profile') and \
        request.user.commercial_profile.access_rights == request.user.commercial_profile.AccessRights.READ_WRITE

    if request.method == 'POST':
        if not can_edit:
            messages.error(request, "You have read-only access.")
            return redirect('commercials_offer_edit_page', slug=slug)
        offer.title = request.POST.get('title')
        offer.description = request.POST.get('description')
        offer.is_active = request.POST.get('is_active') == 'on'
        offer.is_new = request.POST.get('is_new') == 'on'
        offer.save()
        messages.success(request, "Offer updated.")
        return redirect('commercials_offer_edit_page', slug=offer.slug)

    return render(request, 'interns/commercials_offer_edit_page.html', {
        'offer': offer,
        'plans': offer.plans.all(),
        'quotas': offer.wilaya_quotas.all(),
        'can_edit': can_edit,
    })


@login_required(login_url='commercials_login')
def commercials_clients_page(request):
    clients = Client.objects.select_related('user').prefetch_related('locations').all()
    return render(request, 'interns/commercials_clients_page.html', {'clients': clients})


@login_required(login_url='commercials_login')
def commercials_client_detail_page(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    stores = client.locations.all()
    transactions = StoreOfferTransaction.objects.filter(store__in=stores) \
        .select_related('store', 'plan__offer').order_by('-created_at')

    return render(request, 'interns/commercials_client_detail_page.html', {
        'client': client,
        'stores': stores,
        'transactions': transactions,
    })