from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Budget(models.Model):
    VALIDITY_CHOICES = [
        ('30_days', '30 jours'),
        ('custom', 'Utilisateur définit'),
        ('infinite', 'Validité infini'),
    ]
    
    nom = models.CharField(max_length=200, default='Budget')
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='budgets/', null=True, blank=True)
    date_debut = models.DateField(default=timezone.now)
    date_fin = models.DateField(null=True, blank=True)
    validite = models.CharField(max_length=20, choices=VALIDITY_CHOICES, default='30_days')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    montant_restant = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.nom} - {self.montant} FCFA"

    def save(self, *args, **kwargs):
        if not self.pk:  # Si c'est une nouvelle instance
            self.montant_restant = self.montant
        super().save(*args, **kwargs)

class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('create_budget', 'Création de budget'),
        ('edit_budget', 'Modification de budget'),
        ('delete_budget', 'Suppression de budget'),
        ('add_expense', 'Ajout de dépense'),
        ('edit_expense', 'Modification de dépense'),
        ('delete_expense', 'Suppression de dépense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.date}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Notification pour {self.user.username} - {self.date}"

class Depense(models.Model):
    nom = models.CharField(max_length=200)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
    image = models.ImageField(upload_to='depenses/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.ForeignKey(Budget, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nom} - {self.montant} FCFA"

    def save(self, *args, **kwargs):
        if not self.pk and self.budget:  # Si c'est une nouvelle instance et qu'il y a un budget
            # Mettre à jour le montant restant du budget
            self.budget.montant_restant -= self.montant
            self.budget.save()
            
            # Vérifier si le budget est épuisé ou presque épuisé
            pourcentage_restant = (self.budget.montant_restant / self.budget.montant) * 100
            if self.budget.montant_restant <= 0:
                Notification.objects.create(
                    user=self.user,
                    message=f"Votre budget '{self.budget.nom}' est épuisé !",
                    budget=self.budget
                )
            elif pourcentage_restant <= 10:
                Notification.objects.create(
                    user=self.user,
                    message=f"Attention ! Votre budget '{self.budget.nom}' est à {pourcentage_restant:.1f}% de sa capacité.",
                    budget=self.budget
                )
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Dépenses"
