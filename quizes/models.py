from lib2to3.pgen2.token import AT
from numbers import Real
from tkinter.messagebox import QUESTION
from tkinter.tix import REAL
from xml.etree.ElementInclude import default_loader
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import F
from django.urls.base import reverse
from django.utils import translation
from django.utils.translation import ugettext as _
import uuid
from users.models import User
from django.views.generic import edit
from django.utils.text import slugify

QUIZ_CHOICES = (
    ('easy', 'easy'),
    ('medium', 'medium'),
    ('hard', 'hard'),
    ('really hard', 'really hard')
)
# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=50)
    number_of_questions = models.PositiveSmallIntegerField()
    time_to_complete = models.PositiveIntegerField(help_text="How many time can your student complete your quiz?")
    difficulty = models.CharField(max_length=12, choices=QUIZ_CHOICES)
    number_of_questions_to_pass = models.PositiveIntegerField(help_text="How many number of questions does student need to pass your quiz?")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    created_for = models.ManyToManyField('users.User', related_name='created_for')
    author = models.ForeignKey('users.User', related_name='quiz_author', on_delete=models.CASCADE, blank=True)
    attempts = models.PositiveSmallIntegerField(blank=True, default="1")

    class Meta:
        verbose_name = _('Quiz')
        verbose_name_plural = _('Quizes')

    def get_questions(self):
        return self.question_set.all()[:self.number_of_questions]

    def save(self, *args, **kwargs):
        try:
            attempt = Attempts.objects.get(id=self.id)
            attempt.number = self.attempts
            attempt.save()
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} quiz"
    
    
QUESTION_TYPE = (
    ('radio', 'radio'),
    ('text', 'text'),
    ('listbox', 'listbox'),
)
class Question(models.Model):
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=150)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, blank=True)
    type = models.CharField(max_length=9, choices=QUESTION_TYPE, default='radio')
    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
    
    def get_answers(self):
        return self.answer_set.all()

    def __str__(self):
        return self.title


class Answer(models.Model):
    text = models.CharField(max_length=150)
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, blank=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, blank=True)    
    is_correct = models.BooleanField()
    
    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        return self.text

class Attempts(models.Model):
    quiz = models.ForeignKey("Quiz", on_delete=models.CASCADE, related_name="quiz_attempts")
    number = models.PositiveIntegerField()
    user = models.ForeignKey("users.User", related_name="user_attempts", on_delete=models.CASCADE)
    id = models.UUIDField(editable=False, primary_key=True, default=uuid.uuid4)
    
    class Meta:
        verbose_name = _("Attempts")
        verbose_name_plural = _("Attempts")

    def __str__(self):
        return f"{self.number} {self.user} attempts of {self.quiz} quiz "


    def get_absolute_url(self):
        return reverse("Attempts_detail", kwargs={"pk": self.pk})



class Results(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(help_text="How can you rate your score?")
    description = models.TextField(max_length=10000, blank=True)
    attempt = models.PositiveSmallIntegerField(null=True)
    id = models.UUIDField(editable=False, auto_created=True, primary_key=True, default=uuid.uuid4)
    date = models.DateTimeField(editable=False, auto_now_add=True, null=True)

    class Meta:
        verbose_name = _('Results')
        verbose_name_plural = _('Results')

    def get_absolute_url(self):
        return reverse("results", kwargs={"results_slug": self.slug})
    

    def __str__(self):
        return f"Results of {self.quiz} by {self.user}" 

    def get_questions(self):
        return self.question_set.all()[:self.number_of_questions]

    @property
    def get_quiz_attempts(self):
        return self.quiz.attempts


    def save(self, *args, **kwargs):
        slug_str = f"{self.user} {self.score} {self.get_quiz_attempts}"
        self.slug = slugify(slug_str, allow_unicode=True)
        super().save(*args, **kwargs)