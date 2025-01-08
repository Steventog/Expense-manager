from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),  # URL pour la page d'accueil
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='expenses/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='expenses/logout.html'), name='logout'),
    path('budget/add/', views.add_budget, name='add_budget'),
    path('expense/add/', views.add_expense, name='add_expense'),
    path('history/', views.history, name='history'),
    path('stats/', views.stats, name='stats'),
    path('profile/', views.profile, name='profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
]
