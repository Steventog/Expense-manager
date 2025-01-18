from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),  # URL pour la page d'accueil
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='expenses/logout.html'), name='logout'),
    path('home/', views.home, name='home'),
    
    # Budget URLs
    path('budget/add/', views.add_budget, name='add_budget'),
    path('budget/edit/<int:budget_id>/', views.edit_budget, name='edit_budget'),
    path('budget/delete/<int:budget_id>/', views.delete_budget, name='delete_budget'),
    
    # Expense URLs
    path('expense/add/', views.add_expense, name='add_expense'),
    path('history/', views.history, name='history'),
    path('budget-list/', views.budget_list, name='budget_list'),
    path('stats/', views.stats, name='stats'),
    
    # Journal and Notifications
    path('journal/', views.journal, name='journal'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/delete/<int:notification_id>/', views.delete_notification, name='delete_notification'),
    path('notifications/delete-all/', views.delete_all_notifications, name='delete_all_notifications'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
