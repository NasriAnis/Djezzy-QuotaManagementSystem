from django.db import models
from django.contrib.auth.models import User

WILAYA_CHOICES = [
    ('01', 'Adrar'), ('02', 'Chlef'), ('03', 'Laghouat'), ('04', 'Oum El Bouaghi'),
    ('05', 'Batna'), ('06', 'Béjaïa'), ('07', 'Biskra'), ('08', 'Béchar'),
    ('09', 'Blida'), ('10', 'Bouira'), ('11', 'Tamanrasset'), ('12', 'Tébessa'),
    ('13', 'Tlemcen'), ('14', 'Tiaret'), ('15', 'Tizi Ouzou'), ('16', 'Alger'),
    ('17', 'Djelfa'), ('18', 'Jijel'), ('19', 'Sétif'), ('20', 'Saïda'),
    ('21', 'Skikda'), ('22', 'Sidi Bel Abbès'), ('23', 'Annaba'), ('24', 'Guelma'),
    ('25', 'Constantine'), ('26', 'Médéa'), ('27', 'Mostaganem'), ('28', "M'Sila"),
    ('29', 'Mascara'), ('30', 'Ouargla'), ('31', 'Oran'), ('32', 'El Bayadh'),
    ('33', 'Illizi'), ('34', 'Bordj Bou Arréridj'), ('35', 'Boumerdès'),
    ('36', 'El Tarf'), ('37', 'Tindouf'), ('38', 'Tissemsilt'), ('39', 'El Oued'),
    ('40', 'Khenchela'), ('41', 'Souk Ahras'), ('42', 'Tipaza'), ('43', 'Mila'),
    ('44', 'Aïn Defla'), ('45', 'Naâma'), ('46', 'Aïn Témouchent'), ('47', 'Ghardaïa'),
    ('48', 'Relizane'), ('49', 'Timimoun'), ('50', 'Bordj Badji Mokhtar'),
    ('51', 'Ouled Djellal'), ('52', 'Béni Abbès'), ('53', 'In Salah'),
    ('54', 'In Guezzam'), ('55', 'Touggourt'), ('56', 'Djanet'),
    ('57', "El M'Ghair"), ('58', 'El Meniaa'),
]


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return f"{self.user.first_name} {self.user.last_name}"


class Commune(models.Model):
    wilaya_code = models.CharField(max_length=2, choices=WILAYA_CHOICES, db_index=True)
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
        indexes = [models.Index(fields=['wilaya_code', 'name'])]

    def __str__(self):
        return f"{self.name} ({self.get_wilaya_code_display()})"


class Store(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    wilaya = models.CharField(max_length=2, choices=WILAYA_CHOICES)
    comune = models.ForeignKey(Commune, on_delete=models.PROTECT, related_name='stores')
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"

    def __str__(self):
        return f"{self.name} ({self.client})"