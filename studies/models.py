from uuid import uuid4
import uuid
from django.contrib.auth.models import User
from django.db import models
from django import forms
from users import models as users_models
from django.utils.translation import ugettext_lazy as _

#SCHOOL SUBJECT
################################################################################################################################################

class School_Subject(models.Model):
    title = models.CharField(max_length=50)
    teachers = models.ManyToManyField(users_models.User, blank=True, related_name="School_Subject_teachers")
    
    class Meta:
        verbose_name = _('School Subject')

    def __str__(self):
        return self.title

################################################################################################################################################


    
#LESSON
################################################################################################################################################

class Lesson(models.Model):
    title = models.CharField(max_length=20)
    school_subject = models.ForeignKey("School_Subject", on_delete=models.PROTECT, related_name="Lesson_school_subject", blank=True, null=True)
    main_task = models.TextField()
    students = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ForeignKey("users.Study_Group", on_delete=models.SET_NULL, null=True, blank=True)
    id = models.UUIDField(default=uuid4, auto_created=True, editable=False, primary_key=True)
    class Meta:
        verbose_name = _('Lesson')

    def __str__(self):
        return self.title


#################################################################################################################################################


class Task(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


    def __str__(self):
        return f"{self.title} task of {self.lesson} lesson"




################################################################################################################################################

class Mark(models.Model):
    lesson = models.ForeignKey("Lesson", on_delete=models.PROTECT, related_name="Mark_lesson")
    description_of_mark = models.CharField(max_length=100, null=True)
    users = models.ForeignKey(users_models.User, on_delete=models.SET_NULL, related_name="Mark_users", null=True)
    mark = models.CharField(max_length=10)
    school_subject = models.ForeignKey('School_Subject', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Mark')

    def __str__(self):
        return f'Mark of {self.lesson} is {self.mark}'
    
################################################################################################################################################


