from django.contrib import admin
from .models import Lesson, Mark, School_Subject, Task


class LessonInline(admin.TabularInline):
    model = Lesson

class MarkInline(admin.TabularInline):
    model = Mark

# admin.
class TaskInline(admin.TabularInline):
    model = Task


class School_Subject_Admin(admin.ModelAdmin):
    inlines = [LessonInline, MarkInline]

class Lesson_Admin(admin.ModelAdmin):
    inlines = [TaskInline]



admin.site.register(School_Subject, School_Subject_Admin)
admin.site.register(Lesson, Lesson_Admin)
admin.site.register(Task)
admin.site.register(Mark)
# Register your models here.
 