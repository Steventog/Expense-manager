from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Budget, Depense

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

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
