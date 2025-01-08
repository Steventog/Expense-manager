# Gestion des Dépenses - Application Web Django

Une application web de gestion des dépenses personnelles développée avec Django, permettant aux utilisateurs de suivre et gérer leurs dépenses quotidiennes de manière efficace.

## 🌟 Fonctionnalités

- 👤 Système d'authentification complet (inscription, connexion, déconnexion)
- 💰 Ajout et gestion des dépenses
- 📊 Historique des dépenses
- 👤 Gestion de profil utilisateur
- 📱 Interface responsive et moderne
- 🔒 Sécurité des données utilisateur

## 🛠️ Technologies Utilisées

- **Django 5.0** - Framework web Python
- **Bootstrap** - Framework CSS pour le design responsive
- **Crispy Forms** - Pour des formulaires Django élégants
- **SQLite** - Base de données par défaut
- **Pillow** - Traitement d'images pour les photos de profil

## 📋 Prérequis

- Python 3.x
- pip (gestionnaire de paquets Python)
- Environnement virtuel (recommandé)

## ⚙️ Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Steventog/Expense-manager.git
cd Gestion_depenses
```

2. Créez et activez un environnement virtuel :
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Effectuez les migrations :
```bash
python manage.py migrate
```

5. Créez un super utilisateur (optionnel) :
```bash
python manage.py createsuperuser
```

6. Lancez le serveur de développement :
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://127.0.0.1:8000`

## 📁 Structure du Projet

```
Gestion_depenses/
│
├── expense_tracker/        # Configuration principale du projet
├── expenses/              # Application principale
│   ├── templates/         # Templates HTML
│   ├── static/           # Fichiers statiques (CSS, JS, images)
│   ├── models.py         # Modèles de données
│   ├── views.py          # Logique de l'application
│   └── urls.py           # Configuration des URLs
├── media/                # Fichiers uploadés par les utilisateurs
├── static/               # Fichiers statiques globaux
├── manage.py             # Script de gestion Django
└── requirements.txt      # Dépendances du projet
```

## 🔧 Configuration

Les principales configurations se trouvent dans `expense_tracker/settings.py`. Assurez-vous de :

- Configurer votre base de données
- Définir `SECRET_KEY` dans un fichier `.env`
- Configurer les paramètres de messagerie si nécessaire

## 🚀 Déploiement

Pour déployer en production :

1. Configurez les paramètres de production dans `settings.py`
2. Collectez les fichiers statiques :
```bash
python manage.py collectstatic
```
3. Utilisez un serveur WSGI comme Gunicorn
4. Configurez un serveur web (nginx/Apache) comme proxy inverse

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité
3. Commiter vos changements
4. Pousser vers la branche
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue dans le dépôt GitHub.
