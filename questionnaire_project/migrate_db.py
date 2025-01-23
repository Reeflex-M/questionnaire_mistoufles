import os
import django
from django.core.management import call_command

# Configuration pour SQLite (source)
os.environ['DJANGO_SETTINGS_MODULE'] = 'questionnaire_project.settings'
django.setup()

# Créer un dump des données de SQLite
print("Création du dump des données...")
with open('data_dump.json', 'w') as f:
    call_command('dumpdata', exclude=['contenttypes', 'auth.permission'], indent=2, stdout=f)

# Modification du settings.py pour utiliser MySQL
print("Configuration de MySQL...")
from django.conf import settings
settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'questionnaire_db',
    'USER': 'root',
    'PASSWORD': '',
    'HOST': 'localhost',
    'PORT': '3306',
}

# Appliquer les migrations sur MySQL
print("Application des migrations sur MySQL...")
call_command('migrate')

# Charger les données dans MySQL
print("Chargement des données dans MySQL...")
call_command('loaddata', 'data_dump.json')

print("Migration terminée avec succès!")
