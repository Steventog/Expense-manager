from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Budget, Depense

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Désactiver les messages d'aide pour tous les champs
        for field_name, field in self.fields.items():
            field.help_text = None
            
class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['montant', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['nom', 'montant', 'date', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
