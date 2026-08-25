from django.db import models
from django.utils.text import slugify

"""
Models setup:
    OfferCategory (e.g. "Offres Internet")
    └── Offer (e.g. "Djezzy 3Ayla")
        ├── OfferPlan (15Go / 8500 DA)
        ├── OfferPlan (60Go / 9000 DA)
        └── OfferPlan (150Go / 9990 DA)
"""

class OfferCategory(models.Model):
    """eg Offres Prépayées, Offres Internet, Roaming Europe"""

    name = models.CharField(max_length=20, unique=True)
    order = models.PositiveIntegerField(default=0)

    # ordering purpose
    class Meta:
        verbose_name_plural = 'Offer categories'
        ordering = ['order']

    # adding labels for admin panel
    def __str__(self):
        return self.name


class Offer(models.Model):
    """eg Djezzy 3Ayla, DjezzyNet, Nouveau Modem 5G"""

    category = models.ForeignKey(OfferCategory, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ordering purpose
    class Meta:
        ordering = ['category', 'title']

    # auto slugify if empty
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    # adding labels for admin panel
    def __str__(self):
        return self.title


class OfferPlan(models.Model):
    """Pricing tiers within an offer, eg 15Go/8500DA, 60Go/9000DA, 150Go/9990DA"""

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='plans')
    label = models.CharField(max_length=50, blank=True)  # "15Go", "60Go"
    data_amount_gb = models.PositiveIntegerField(null=True, blank=True)
    price_da = models.DecimalField(max_digits=10, decimal_places=2)
    validity_days = models.PositiveIntegerField(default=30)

    # other config can be set via json dynamically
    features = models.JSONField(default=dict, blank=True)

    # ordering purpose
    class Meta:
        ordering = ['price_da']

    # adding labels for admin panel
    def __str__(self):
        return f"{self.offer.title} — {self.label or self.data_amount_gb}Go — {self.price_da} DA"