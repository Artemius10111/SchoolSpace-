from django.contrib import admin
from .models import Quiz, Question, Answer, Results, Attempts
class AnswerInline(admin.TabularInline):
    model = Answer

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


class QuestionInline(admin.TabularInline):
    model = Question

class AttemptsInline(admin.TabularInline):
    model = Attempts

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, AnswerInline, AttemptsInline]
    # readonly_fields = ('authors',)

class ResultsAdmin(admin.ModelAdmin):
    model = Results
    

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Quiz, QuizAdmin)
admin.site.register(Results, ResultsAdmin)
admin.site.register(Attempts)
# Register your models here.
