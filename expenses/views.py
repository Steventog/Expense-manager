from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import UserRegistrationForm, BudgetForm, DepenseForm, UserProfileForm, BudgetAdjustForm
from .models import Budget, Depense, Notification, ActionLog
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from decimal import Decimal

def accueil(request):
    return render(request, 'expenses/accueil.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'expenses/register.html', {'form': form})

@login_required
def home(request):
    # Récupérer tous les budgets
    budgets = Budget.objects.filter(
        user=request.user
    ).order_by('-date_debut')

    # Récupérer les dépenses récentes (limité à 5)
    expenses = Depense.objects.filter(
        user=request.user
    ).select_related('budget').order_by('-date')[:5]

    context = {
        'budgets': budgets,
        'expenses': expenses,
    }
    
    return render(request, 'expenses/home.html', context)

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST, request.FILES)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.date_fin = form.cleaned_data.get('date_fin')
            budget.save()
            
            ActionLog.objects.create(
                user=request.user,
                action='create_budget',
                description=f"Création du budget '{budget.nom}' de {budget.montant} FCFA"
            )
            
            messages.success(request, 'Budget créé avec succès!')
            return redirect('home')
    else:
        form = BudgetForm()
    return render(request, 'expenses/add_budget.html', {'form': form})

@login_required
def edit_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    
    if request.method == 'POST':
        form = BudgetAdjustForm(request.POST)
        if form.is_valid():
            montant_ajout = form.cleaned_data['montant_ajout']
            
            # Mettre à jour les montants
            budget.montant += montant_ajout
            budget.montant_restant += montant_ajout
            budget.save()
            
            # Créer une entrée dans le journal
            ActionLog.objects.create(
                user=request.user,
                action='edit_budget',
                description=f"Ajout de {montant_ajout} FCFA au budget '{budget.nom}'"
            )
            
            messages.success(request, f'Budget ajusté avec succès! Ajout de {montant_ajout} FCFA')
            return redirect('home')
    else:
        form = BudgetAdjustForm()
    
    return render(request, 'expenses/adjust_budget.html', {
        'form': form,
        'budget': budget
    })

@login_required
def delete_budget(request, budget_id):
    budget = get_object_or_404(Budget, id=budget_id, user=request.user)
    if request.method == 'POST':
        nom_budget = budget.nom
        budget.delete()
        
        ActionLog.objects.create(
            user=request.user,
            action='delete_budget',
            description=f"Suppression du budget '{nom_budget}'"
        )
        
        messages.success(request, 'Budget supprimé avec succès!')
        return redirect('home')
    return render(request, 'expenses/delete_budget.html', {'budget': budget})

@login_required
def add_expense(request):
    if request.method == 'POST':
        form = DepenseForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            depense = form.save(commit=False)
            depense.user = request.user
            
            # Vérifier si un budget est sélectionné
            budget = form.cleaned_data.get('budget')
            if budget:
                # Vérifier si le montant de la dépense ne dépasse pas le budget restant
                if depense.montant > budget.montant_restant:
                    messages.error(request, f'Le budget "{budget.nom}" est insuffisant! (Reste: {budget.montant_restant} FCFA)')
                    
                    # Créer une notification
                    Notification.objects.create(
                        user=request.user,
                        message=f'Attention: Tentative de dépense de {depense.montant} FCFA alors que le budget "{budget.nom}" ne dispose que de {budget.montant_restant} FCFA',
                        lu=False
                    )
                    
                    return render(request, 'expenses/add_expense.html', {'form': form})
            
            # Sauvegarder la dépense (la mise à jour du budget est gérée dans le modèle Depense)
            depense.save()
            
            # Créer une entrée dans le journal d'activité
            ActionLog.objects.create(
                user=request.user,
                action='add_expense',
                description=f"Ajout d'une dépense de {depense.montant} FCFA pour '{depense.nom}'"
            )
            
            messages.success(request, 'Dépense ajoutée avec succès!')
            return redirect('home')
    else:
        form = DepenseForm(request.user)
        
        # Vérifier si l'utilisateur a des budgets
        if not Budget.objects.filter(user=request.user).exists():
            messages.warning(request, 'Vous devez créer un budget avant d\'ajouter une dépense.')
            return redirect('add_budget')
            
    return render(request, 'expenses/add_expense.html', {'form': form})

@login_required
def journal(request):
    actions = ActionLog.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/journal.html', {'actions': actions})

@login_required
def notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-date')
    return render(request, 'expenses/notifications.html', {'notifications': notifications})

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.lu = True
    notification.save()
    return JsonResponse({'status': 'success'})

@login_required
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.delete()
    return JsonResponse({'status': 'success'})

@login_required
def delete_all_notifications(request):
    Notification.objects.filter(user=request.user).delete()
    return JsonResponse({'status': 'success'})

@login_required
def stats(request):
    # Récupérer toutes les dépenses et les budgets
    all_expenses = Depense.objects.filter(
        user=request.user
    ).order_by('date')

    all_budgets = Budget.objects.filter(
        user=request.user
    ).order_by('date_debut')

    # Créer une liste de toutes les dates uniques pour l'axe X
    all_dates = set()
    for expense in all_expenses:
        all_dates.add(expense.date)
    for budget in all_budgets:
        all_dates.add(budget.date_debut)
        if budget.date_fin:
            all_dates.add(budget.date_fin)
    
    # Trier les dates
    all_dates = sorted(list(all_dates))

    # Préparer les données pour le graphique
    expense_data = []
    budget_data = []
    expense_labels = []

    # Pour chaque date, calculer le total des dépenses et des budgets actifs
    for date in all_dates:
        # Total des dépenses pour cette date
        daily_expenses = sum(expense.montant for expense in all_expenses.filter(date=date))

        # Total des budgets actifs pour cette date
        active_budgets_sum = sum(
            budget.montant for budget in all_budgets.filter(
                date_debut__lte=date
            ).filter(Q(date_fin__gte=date) | Q(date_fin__isnull=True))
        )

        expense_data.append(float(daily_expenses))
        budget_data.append(float(active_budgets_sum))
        expense_labels.append(date.strftime('%Y-%m-%d'))

    # Calculer le montant restant pour chaque date
    remaining_data = [max(0, b - e) for b, e in zip(budget_data, expense_data)]

    context = {
        'expense_labels': expense_labels,
        'expense_data': expense_data,
        'budget_data': budget_data,
        'remaining_data': remaining_data,
    }
    return render(request, 'expenses/stats.html', context)

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
def budget_list(request):
    # Récupérer tous les budgets de l'utilisateur
    budgets = Budget.objects.filter(user=request.user).order_by('-date_debut')
    
    # Pour chaque budget, récupérer ses dépenses
    budget_details = []
    for budget in budgets:
        expenses = Depense.objects.filter(
            user=request.user,
            budget=budget
        ).order_by('-date')
        
        total_expenses = expenses.aggregate(total=Sum('montant'))['total'] or 0
        
        budget_details.append({
            'budget': budget,
            'expenses': expenses,
            'total_expenses': total_expenses,
        })
    
    # Dépenses sans budget
    unbudgeted_expenses = Depense.objects.filter(
        user=request.user,
        budget__isnull=True
    ).order_by('-date')
    
    total_unbudgeted = unbudgeted_expenses.aggregate(total=Sum('montant'))['total'] or 0
    
    context = {
        'budget_details': budget_details,
        'unbudgeted_expenses': unbudgeted_expenses,
        'total_unbudgeted': total_unbudgeted,
    }
    
    return render(request, 'expenses/budget_list.html', context)

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
