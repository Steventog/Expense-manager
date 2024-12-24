from django.contrib import admin
from .models import Budget, Depense

# Register your models here.

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'montant', 'date')
    list_filter = ('date', 'user')
    search_fields = ('user__username',)

@admin.register(Depense)
class DepenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'montant', 'date')
    list_filter = ('date', 'user')
    search_fields = ('nom', 'user__username')
