
from django.db.models import fields
from django.db.models.base import Model
from .models import Quiz 
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django import forms 
from users.models import User

QUIZ_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
    ('really hard', 'really hard')
)

class QuizCreateForm(ModelForm):
    difficulty = forms.ChoiceField(
        choices = QUIZ_CHOICES,
        widget=forms.RadioSelect(attrs={
        }),
    )

    class Meta:
        model = Quiz
        fields = "__all__"
        widgets = {
            'author': forms.HiddenInput()
        }
    

class QuizUpdateForm(ModelForm):
    class Meta: 
        model = Quiz 
        fields = '__all__'