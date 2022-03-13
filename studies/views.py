from audioop import reverse
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import Lesson, Task
from django.forms.models import modelformset_factory
from .forms import LessonForm, TaskForm
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.forms.models import modelformset_factory
from users.models import Study_Group, School
# class LessonAddView(TemplateView):
#     template_name = 'studies/create_lesson.html'
#     form_class = LessonForm
#     def get(self, *args, **kwargs):
#         form = LessonForm()
#         formset = LessonFormSet(queryset=Lesson.objects.none())
#         return self.render_to_response({'lesson_formset': formset, 'form': form})

#     def post(self, *args, **kwargs):
#         form = LessonForm()
#         formset = LessonFormSet(data=self.request.POST)

#         if formset.is_valid() and form.is_valid():
#             formset.save()
#             form.save()
#             return redirect(reverse_lazy("home")) 

#         return self.render_to_response({'lesson_formset': formset, 'form': form})



class LessonListView(ListView):
    model = Lesson 
    template_name = 'studies/lesson_list.html'
    paginate_by = 5
    success_url = reverse_lazy('lesson_list')

    context_object_name = 'lessons'

    def get_queryset(self):
        return list(reversed(Lesson.objects.all()))

def lesson_view(request, pk):
    lesson = Lesson.objects.get(id=pk)
    tasks = Task.objects.filter(lesson=lesson)
    return render(request, 'studies/lesson_description.html', {'lesson': lesson, 'tasks': tasks})


def lesson_add_view(request):
    if request.method == "POST":
        TaskFormSet = modelformset_factory(Task, fields=('title',), extra=3, max_num=5)
        formset = TaskFormSet(request.POST, queryset=Task.objects.none())
        form_parent = LessonForm(request.POST, request.FILES)
        context = {
            'task_form_set': formset,
            'form_parent': form_parent,
        }
        if all([form_parent.is_valid(), formset.is_valid()]):
            parent = form_parent.save(commit=False)
            parent.save()
            children = formset.save(commit=False)
            for child in children:
                child.lesson = parent
                child.save()
    TaskFormSet = modelformset_factory(Task, fields=('title',), extra=3)
    formset = TaskFormSet(None, queryset=Task.objects.none())
    form_parent = LessonForm(None)
    context = {
        'task_form_set': formset,
        'form_parent': form_parent,
    }
    return render(request, "studies/create_lesson.html", context)

def school_view(request):
    try:
        study_group = Study_Group.objects.get(users=request.user)
        school = School.objects.get(school_groups=study_group)
        context = {
            "school": school,
        }
        return render(request, "studies/school_view.html", context)
    except:
        return render(request, "studies/school_view.html")