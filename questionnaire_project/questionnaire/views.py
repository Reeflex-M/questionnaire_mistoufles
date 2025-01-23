from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Question, Answer, Respondent, Questionnaire
from .serializers import QuestionSerializer, AnswerSerializer, RespondentSerializer, QuestionnaireSerializer
from django.utils import timezone

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class RespondentViewSet(viewsets.ModelViewSet):
    queryset = Respondent.objects.all()
    serializer_class = RespondentSerializer
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        search_term = request.query_params.get('q', '')
        if search_term:
            respondents = self.queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term)
            )
            serializer = self.get_serializer(respondents, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=True, methods=['get'])
    def questionnaires(self, request, pk=None):
        """Récupère tous les questionnaires d'un répondant"""
        respondent = self.get_object()
        questionnaires = respondent.questionnaires.all()
        data = []
        for q in questionnaires:
            data.append({
                'id': q.id,
                'submitted_at': q.submitted_at,
                'is_approved': q.is_approved,
                'approved_by': q.approved_by.username if q.approved_by else None,
                'answers': q.answers
            })
        return Response(data)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    @action(detail=False, methods=['get'])
    def by_respondent(self, request):
        respondent_id = request.query_params.get('respondent_id')
        if respondent_id:
            answers = self.queryset.filter(respondent_id=respondent_id)
            serializer = self.get_serializer(answers, many=True)
            return Response(serializer.data)
        return Response({'error': 'respondent_id is required'}, status=status.HTTP_400_BAD_REQUEST)

class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer

    @action(detail=False, methods=['post'])
    def submit_questionnaire(self, request):
        data = request.data
        
        # Créer le questionnaire avec toutes les informations
        questionnaire = Questionnaire.objects.create(
            # Informations personnelles
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            phone=data.get('phone'),
            address=data.get('address'),
            postal_code=data.get('postal_code'),
            city=data.get('city'),
            
            # Informations générales
            living_context=data.get('living_context'),
            professional_activity=data.get('professional_activity'),
            housing_type=data.get('housing_type'),
            has_garden=data.get('has_garden', False),
            garden_details=data.get('garden_details'),
            
            # Toutes les réponses au questionnaire
            answers=data.get('answers', {})
        )
        
        return Response({
            'status': 'success',
            'questionnaire_id': questionnaire.id
        }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Recherche des questionnaires par nom/prénom"""
        search_term = request.query_params.get('q', '')
        if search_term:
            questionnaires = self.queryset.filter(
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(email__icontains=search_term)
            )
            serializer = self.get_serializer(questionnaires, many=True)
            return Response(serializer.data)
        return Response([])

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Récupère tous les questionnaires en attente d'approbation"""
        questionnaires = self.queryset.filter(is_approved=False)
        serializer = self.get_serializer(questionnaires, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approuve un questionnaire"""
        questionnaire = self.get_object()
        questionnaire.is_approved = True
        questionnaire.approved_by = request.user
        questionnaire.approved_at = timezone.now()
        questionnaire.save()
        return Response({'status': 'success'})
