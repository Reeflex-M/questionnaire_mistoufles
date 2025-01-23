from rest_framework import serializers
from .models import Question, Answer, Respondent

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class RespondentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respondent
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.text', read_only=True)
    respondent_name = serializers.CharField(source='respondent.__str__', read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'question', 'question_text', 'respondent', 'respondent_name', 'text', 'created_at']

class QuestionnaireResponseSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    answers = serializers.DictField(child=serializers.CharField())
