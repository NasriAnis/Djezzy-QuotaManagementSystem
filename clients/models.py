from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"

class Store(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    comune = models.CharField(max_length=100)
    wilaya = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return f"{self.name} ({self.client.name})"