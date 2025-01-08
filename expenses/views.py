from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegistrationForm, BudgetForm, DepenseForm, UserProfileForm
from .models import Budget, Depense
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from django.contrib.auth import update_session_auth_hash

def accueil(request):
    return render(request, 'expenses/accueil.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Compte créé pour {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'expenses/register.html', {'form': form})

@login_required
def home(request):
    current_date = timezone.now().date()
    current_month_start = current_date.replace(day=1)
    next_month = current_date.replace(day=28) + timedelta(days=4)
    current_month_end = next_month - timedelta(days=next_month.day)

    # Get current month's budget
    current_budget = Budget.objects.filter(
        user=request.user,
        date__year=current_date.year,
        date__month=current_date.month
    ).first()

    # Get current month's expenses
    expenses = Depense.objects.filter(
        user=request.user,
        date__range=[current_month_start, current_month_end]
    ).order_by('-date')

    total_expenses = expenses.aggregate(Sum('montant'))['montant__sum'] or 0

    context = {
        'budget': current_budget,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'remaining_budget': (current_budget.montant - total_expenses) if current_budget else 0
    }
    return render(request, 'expenses/home.html', context)

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget ajouté avec succès!')
            return redirect('home')
    else:
        form = BudgetForm()
    return render(request, 'expenses/budget_form.html', {'form': form})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = DepenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Dépense ajoutée avec succès!')
            return redirect('home')
    else:
        form = DepenseForm()
    return render(request, 'expenses/expense_form.html', {'form': form})

@login_required
def history(request):
    # Get all years and months with expenses
    years_months = Depense.objects.filter(user=request.user)\
        .dates('date', 'month', order='DESC')

    # Get selected year and month from query parameters
    selected_year = request.GET.get('year')
    selected_month = request.GET.get('month')

    # Filter expenses
    expenses = Depense.objects.filter(user=request.user)
    if selected_year:
        expenses = expenses.filter(date__year=selected_year)
    if selected_month:
        expenses = expenses.filter(date__month=selected_month)

    # Recherche par nom ou montant
    search_query = request.GET.get('search', '')
    if search_query:
        expenses = expenses.filter(
            Q(nom__icontains=search_query) |
            Q(montant__icontains=search_query)
        )

    # Order by date
    expenses = expenses.order_by('-date')

    # Get total for filtered expenses
    total = expenses.aggregate(Sum('montant'))['montant__sum'] or 0

    # Get budget for selected period if exists
    budget = None
    if selected_year and selected_month:
        budget = Budget.objects.filter(
            user=request.user,
            date__year=selected_year,
            date__month=selected_month
        ).first()

    context = {
        'years_months': years_months,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'expenses': expenses,
        'total': total,
        'budget': budget
    }
    return render(request, 'expenses/history.html', context)

@login_required
def stats(request):
    # Récupérer les dépenses de l'utilisateur
    expenses = Depense.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)

    # Agréger les dépenses par mois
    monthly_expenses = expenses.annotate(
        month=ExtractMonth('date'),
        year=ExtractYear('date')
    ).values('year', 'month').annotate(
        total=Sum('montant')
    ).order_by('year', 'month')

    # Préparer les données pour Chart.js
    expense_labels = []
    expense_data = []
    budget_data = []

    for entry in monthly_expenses:
        month_name = f"{entry['year']}-{entry['month']:02d}"
        expense_labels.append(month_name)
        expense_data.append(float(entry['total']))
        
        # Récupérer le budget correspondant au mois
        month_budget = budgets.filter(
            date__year=entry['year'],
            date__month=entry['month']
        ).first()
        budget_amount = float(month_budget.montant) if month_budget else 0
        budget_data.append(budget_amount)

    context = {
        'expense_labels': expense_labels,
        'expense_data': expense_data,
        'budget_data': budget_data,
    }
    return render(request, 'expenses/stats.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Statistiques de l'utilisateur
    expenses = Depense.objects.filter(user=request.user)
    total_expenses = expenses.aggregate(total=Sum('montant'))['total'] or 0
    expense_count = expenses.count()
    
    # Dernières dépenses
    recent_expenses = expenses.order_by('-date')[:5]
    
    context = {
        'form': form,
        'total_expenses': total_expenses,
        'expense_count': expense_count,
        'recent_expenses': recent_expenses,
    }
    return render(request, 'expenses/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été modifié avec succès!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'expenses/change_password.html', {'form': form})
