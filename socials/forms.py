from .models import Post, Comment
from django.forms import ModelForm
from django import forms
from django.shortcuts import redirect, render



class PostCreateForm(forms.ModelForm):
    class Meta:
        fields = '__all__'
        model = Post
        widgets = {
            'author': forms.HiddenInput(),
        }
        
class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
        widgets = {
            'author': forms.HiddenInput(),
            'post': forms.HiddenInput(), 
        }