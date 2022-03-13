from django.forms import modelformset_factory
from django import forms
from studies.models import Lesson, Task


class LessonForm(forms.ModelForm):
    main_task = forms.TextInput()
    class Meta:
        model = Lesson
        fields = ("title", "main_task")
        widgets = {
          'main_task': forms.Textarea(attrs={'rows':7, 'cols':30}),
        }

class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ('title',)
        widgets = {
          'title': forms.Textarea(attrs={'rows':2, 'cols':30}),
        }
