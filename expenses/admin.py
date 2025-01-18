from django.contrib import admin
from .models import Budget, Depense, Notification, ActionLog

# Register your models here.

class DepenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'montant', 'date', 'budget')
    list_filter = ('date', 'user', 'budget')
    search_fields = ('nom', 'user__username')

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom', 'montant', 'montant_restant', 'date_debut', 'date_fin', 'validite')
    list_filter = ('date_debut', 'validite', 'user')
    search_fields = ('nom', 'user__username')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'date', 'lu', 'budget')
    list_filter = ('lu', 'date', 'user')
    search_fields = ('message', 'user__username')

class ActionLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'description', 'date')
    list_filter = ('action', 'date', 'user')
    search_fields = ('description', 'user__username')

admin.site.register(Depense, DepenseAdmin)
admin.site.register(Budget, BudgetAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
