from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Depense, Budget
from django.utils import timezone

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter les classes Bootstrap à tous les champs
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field_name].label
            })

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['nom', 'montant', 'image', 'validite', 'date_debut']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom du budget'
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Montant du budget'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'validite': forms.Select(attrs={
                'class': 'form-control',
                'id': 'validite-select'
            }),
            'date_debut': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

    date_fin = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'id': 'date-fin-input'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        validite = cleaned_data.get('validite')
        date_debut = cleaned_data.get('date_debut')
        date_fin = cleaned_data.get('date_fin')

        if validite == '30_days':
            # Calculer automatiquement la date de fin pour 30 jours
            cleaned_data['date_fin'] = date_debut + timezone.timedelta(days=30)
        elif validite == 'custom':
            if not date_fin:
                raise forms.ValidationError("La date de fin est requise pour une validité personnalisée")
            if date_fin <= date_debut:
                raise forms.ValidationError("La date de fin doit être postérieure à la date de début")
        elif validite == 'infinite':
            cleaned_data['date_fin'] = None

        return cleaned_data

class BudgetAdjustForm(forms.Form):
    montant_ajout = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Montant à ajouter'
        })
    )

class DepenseForm(forms.ModelForm):
    class Meta:
        model = Depense
        fields = ['nom', 'montant', 'date', 'image', 'budget']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description de la dépense'
            }),
            'montant': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Montant'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'budget': forms.Select(attrs={
                'class': 'form-control'
            })
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['budget'].queryset = Budget.objects.filter(user=user)

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Nom d\'utilisateur',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
