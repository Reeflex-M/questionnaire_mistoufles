import os
import django
from django.core.management import call_command

# Configuration Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'questionnaire_project.settings'
django.setup()

# Appliquer les migrations sur MySQL
print("Application des migrations sur MySQL...")
call_command('migrate')

print("Migration terminée!")
