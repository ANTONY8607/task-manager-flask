# Application d'Agenda pour la Gestion des Tâches

Une application web moderne pour gérer vos tâches quotidiennes, développée avec Flask.

## Fonctionnalités

- Création, modification et suppression de tâches
- Catégorisation des tâches (Personnel, Professionnel, Études)
- Gestion des priorités (Haute, Moyenne, Basse)
- Système d'authentification utilisateur
- Interface responsive et moderne

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

1. Clonez ce dépôt :
```bash
git clone [URL_DU_REPO]
cd [NOM_DU_DOSSIER]
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
```

3. Activez l'environnement virtuel :
- Windows :
```bash
venv\Scripts\activate
```
- Linux/MacOS :
```bash
source venv/bin/activate
```

4. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

1. Créez un fichier `.env` à la racine du projet :
```
SECRET_KEY=votre-clé-secrète
DATABASE_URL=sqlite:///agenda.db
```

## Lancement de l'application

1. Initialisez la base de données :
```bash
flask db upgrade
```

2. Lancez l'application :
```bash
python run.py
```

3. Accédez à l'application dans votre navigateur à l'adresse : `http://localhost:5000`

## Utilisation

1. Créez un compte utilisateur en cliquant sur "Inscription"
2. Connectez-vous avec vos identifiants
3. Commencez à créer et gérer vos tâches !

## Structure du Projet

```
agenda/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── auth.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
│       ├── auth/
│       ├── task/
│       └── base.html
├── requirements.txt
└── run.py
```

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou à proposer une pull request.

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
