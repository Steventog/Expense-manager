from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Budget(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Budget de {self.montant} FCFA pour {self.date}"

class Depense(models.Model):
    nom = models.CharField(max_length=200)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='depenses/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} - {self.montant} FCFA"

    class Meta:
        verbose_name_plural = "Dépenses"
