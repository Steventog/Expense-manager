# Schéma de la Base de Données - Expense Manager

## Modèle Conceptuel de Données (MCD)

```
                                    UTILISATEUR (User)
                                    ---------------
                                    #id
                                    username
                                    password
                                    email
                                    first_name
                                    last_name
                                    |
                    ________________|________________
                    |              |                |
                    |              |                |
                    ▼              ▼                ▼
            BUDGET                DEPENSE           NOTIFICATION
            ------                -------           ------------
            #id                   #id               #id
            nom                   nom               message
            montant              montant            date
            image                date               lu
            date_debut           image              #budget_id (0,1)
            date_fin (0,1)       #user_id          #user_id
            validite             #budget_id (0,1)
            #user_id             
            montant_restant      
                    |
                    |
                    ▼
            ACTIONLOG
            ---------
            #id
            action
            description
            date
            #user_id
```

## Légende
- Une flèche simple (▼) indique une relation 1,n (un-à-plusieurs)
- (0,1) indique une relation optionnelle
- # indique une clé primaire ou étrangère

## Relations Détaillées

### 1. Utilisateur - Budget
- Un utilisateur peut avoir plusieurs budgets (1,n)
- Chaque budget appartient à un seul utilisateur (1,1)

### 2. Utilisateur - Dépense
- Un utilisateur peut avoir plusieurs dépenses (1,n)
- Chaque dépense appartient à un seul utilisateur (1,1)

### 3. Budget - Dépense
- Un budget peut avoir plusieurs dépenses (1,n)
- Une dépense peut être associée à un seul budget ou à aucun (0,1)

### 4. Utilisateur - Notification
- Un utilisateur peut avoir plusieurs notifications (1,n)
- Chaque notification appartient à un seul utilisateur (1,1)

### 5. Budget - Notification
- Un budget peut avoir plusieurs notifications (1,n)
- Une notification peut être liée à un budget ou à aucun (0,1)

### 6. Utilisateur - ActionLog
- Un utilisateur peut avoir plusieurs entrées dans le journal d'actions (1,n)
- Chaque entrée du journal appartient à un seul utilisateur (1,1)

## Caractéristiques des Entités

### 1. Budget
- Gère les montants avec validité (30 jours, infinie, ou personnalisée)
- Suit le montant restant automatiquement
- Permet l'ajout d'une image
- Types de validité :
  - 30 jours
  - Personnalisée
  - Infinie

### 2. Dépense
- Peut être liée ou non à un budget
- Met à jour automatiquement le montant restant du budget
- Génère des notifications quand le budget atteint des seuils critiques
- Supporte les images pour les reçus

### 3. Notification
- Système d'alerte pour les budgets
- Peut être marquée comme lue/non lue
- Peut être liée à un budget spécifique
- Générée automatiquement lors d'événements importants :
  - Budget épuisé
  - Budget proche de l'épuisement (10%)

### 4. ActionLog
- Journal des actions utilisateur
- Types d'actions prédéfinis :
  - Création de budget
  - Modification de budget
  - Suppression de budget
  - Ajout de dépense
  - Modification de dépense
  - Suppression de dépense
- Horodatage automatique de chaque action

## Fonctionnalités Clés
- Suivi des budgets et dépenses
- Système de notification
- Journalisation des actions
- Support pour les images (reçus, justificatifs)
- Gestion flexible des périodes de validité des budgets
- Calcul automatique des montants restants
- Alertes automatiques pour les seuils critiques
