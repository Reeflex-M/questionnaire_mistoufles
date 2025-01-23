import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionnaire_project.settings')
django.setup()

from questionnaire.models import Question

# Liste des questions à ajouter
questions = [
    "Quel est votre âge ?",
    "Quelle est votre profession ?",
    "Dans quelle ville habitez-vous ?",
    "Quel est votre niveau d'études ?",
    "Quel est votre domaine d'expertise ?",
    "Combien d'années d'expérience avez-vous dans votre domaine ?",
    "Quelles sont vos principales compétences ?",
    "Quels sont vos objectifs professionnels ?",
    "Quelles sont vos disponibilités ?",
    "Avez-vous des commentaires supplémentaires ?"
]

# Ajout des questions
for question_text in questions:
    Question.objects.get_or_create(text=question_text)

print("Questions ajoutées avec succès !")
