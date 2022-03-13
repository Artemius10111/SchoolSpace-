from django.contrib.auth import forms, get_user_model
from django.db.models.fields import CharField
from .models import School, User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
class CustomUserCreationForm(UserCreationForm):
    CHOICES = (
        ('user', 'user'),
        ('master', 'master'),
    )
    role = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'age', 'role')
        
class CustomUserChangeForm(forms.ModelForm):


    class Meta:
        model = User
        labels = {
        "profile_pic": "Profile picture",
    }
        fields = ('first_name', 'last_name', 'email', 'profile_pic')
    
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields["profile_pic"].widget.attrs.update({'class': 'form-control-file',})


class SchoolCreateForm(forms.ModelForm):
    

    class Meta:
        model = School
        fields = "__all__"
