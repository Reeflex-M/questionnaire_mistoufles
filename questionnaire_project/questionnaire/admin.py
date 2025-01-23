from django.contrib import admin
from django.utils import timezone
from .models import Question, Answer, Respondent, Questionnaire

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'created_at')
    search_fields = ('text',)
    list_filter = ('created_at',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'created_at')
    search_fields = ('text', 'question__text')
    list_filter = ('created_at', 'question')

@admin.register(Respondent)
class RespondentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    list_filter = ('created_at', 'living_context')
    readonly_fields = ('created_at',)

@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'city', 'created_at', 'is_approved')
    list_filter = ('created_at', 'is_approved', 'city', 'living_context', 'housing_type')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city')
    readonly_fields = ('created_at', 'updated_at', 'answers_display')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'address', 'postal_code', 'city')
        }),
        ('Informations générales', {
            'fields': ('living_context', 'professional_activity', 'housing_type', 'has_garden', 'garden_details')
        }),
        ('Réponses au questionnaire', {
            'fields': ('answers_display',)
        }),
        ('Administration', {
            'fields': ('is_approved', 'approved_by', 'approved_at', 'notes', 'created_at', 'updated_at')
        })
    )

    def answers_display(self, obj):
        """Affiche les réponses de manière formatée"""
        if not obj.answers:
            return "Aucune réponse"
            
        html = ["<div style='padding: 10px;'>"]
        
        # Parcourir toutes les sections de réponses
        for section, answers in obj.answers.items():
            html.append(f"<h3 style='color: #2563EB; margin-top: 20px;'>{section.replace('_', ' ').title()}</h3>")
            
            if isinstance(answers, dict):
                html.append("<ul>")
                for key, value in answers.items():
                    if isinstance(value, dict):
                        html.append(f"<li><strong>{key}:</strong>")
                        html.append("<ul>")
                        for sub_key, sub_value in value.items():
                            html.append(f"<li><strong>{sub_key}:</strong> {sub_value}</li>")
                        html.append("</ul></li>")
                    else:
                        html.append(f"<li><strong>{key}:</strong> {value}</li>")
                html.append("</ul>")
            else:
                html.append(f"<p>{answers}</p>")
            
        html.append("</div>")
        return ''.join(html)
    
    answers_display.short_description = "Réponses au questionnaire"
    answers_display.allow_tags = True

    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get('is_approved') and not obj.approved_by:
            obj.approved_by = request.user
            obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)
