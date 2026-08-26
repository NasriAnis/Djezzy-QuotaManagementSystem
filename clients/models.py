from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

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