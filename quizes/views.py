from site import PREFIXES
from django.forms import modelformset_factory
from django.urls import reverse
from typing import List
from unittest import result
from django import template
from django.db.models import fields
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView
from users.models import User
from .models import Answer, Attempts, Question, Quiz, Results
from .forms import QuizCreateForm, QuizUpdateForm
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from users.forms import CustomUserCreationForm
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone

# Create your views here.

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizes/quiz_list.html'
    paginate_by = 1
    success_url = reverse_lazy('quiz_list')

    def get_queryset(self):
        return list(reversed(Quiz.objects.filter(
            created_for=self.request.user
        )))

class ResultsListView(ListView):
    model = Results
    template_name = 'quizes/quiz_results.html'
    paginate_by = 7
    success_url = reverse_lazy('results_list')

    context_object_name = 'user_results'


    def get_queryset(self):
        return list(reversed(Results.objects.filter(
            user=self.request.user
        )))
    

def results_detail_view(request, pk):
    results = Results.objects.get(id=pk)
    return render(request, 'quizes/quiz_results_detail.html', {'results': results})

def quiz_view(request, pk):
    quiz = Quiz.objects.get(id=pk)
    can_edit = str(request.user) in [str(i) for i in (quiz.authors.all())]
    try:
        attempt = Attempts.objects.get(quiz=quiz, user=request.user)
        return render(request, 'quizes/quiz_description.html', {'obj': quiz, 'attempts': attempt, 'can_edit': can_edit})
    except Attempts.DoesNotExist:
        return render(request, 'quizes/quiz_description.html', {'obj': quiz})
    
        
def quiz_data_view(request, pk, url=None):
    quiz = Quiz.objects.get(id=pk)
    questions = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})

    return JsonResponse({
            'data': questions,
            'time': quiz.time_to_complete,
            'url': url,
        })
def quiz_action_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    attempts = Attempts.objects.get(quiz=quiz, user=request.user)
    if attempts.number <= 0: 
        return redirect('quiz_list')
    return render(request, 'quizes/quiz_started.html', {'obj': quiz})


def quiz_save_view(request, pk):
    data = dict(request.POST)
    time = ''.join(data['time_sign'])
    del data['csrfmiddlewaretoken']
    questions = []
    for k in data.keys():
        try:
            question = Question.objects.get(text=k)
            questions.append(question)
        except:
            pass
        

    user = request.user
    quiz = Quiz.objects.get(pk=pk)

    score = 0
    number_of_questions = quiz.number_of_questions
    multiplier = 100 / number_of_questions
    results = {}
    correct_answer = None

    for q in questions:
        a_selected = request.POST.get(q.text)
        if a_selected != "":
            
            question_answers = Answer.objects.filter(question=q)
            for a in question_answers:
                if a_selected == a.text:
                    if a.is_correct:
                        score += 1
        
    score_ = score * multiplier

    description = f"""
Score is {score_}, \n
Number of questions is {score}/{number_of_questions}, \n
Time left after completing {quiz.title} {time}
                    """
    try:
        
        attempts = Attempts.objects.get(quiz=quiz, user=request.user)
        result = Results.objects.create(quiz=quiz, user=user, score=score_, description=description, attempt=attempts.number)
        attempts.number -= 1
        attempts.save()
    except:
        pass 
    url = reverse("result_detail", kwargs = {'pk': result.id})
    quiz_data_view(request, url=url, pk=quiz.id)
    return HttpResponse('ok')


class UpdateQuizView(SuccessMessageMixin, generic.UpdateView):
    template_name = 'quizes/quiz_update.html/'
    form_class = QuizUpdateForm
    model = Quiz
    success_message = "Your quiz was successfully updated!"
    success_url = reverse_lazy('quiz_update')

def update_quiz_view(request, pk):
    if request.method == 'POST':
        form = QuizUpdateForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'quizes/quiz_update.html', {'form': form})
    else:
        form = QuizUpdateForm
        return render(request, 'quizes/quiz_update.html', {'form': form})

def results_quiz_view(request, results_slug, pk):
    result = Results.objects.get(slug=results_slug)
    return render(request, 'quizes/quiz_results.html', {'obj': result})

@login_required
@permission_required('quizes.add_quiz', raise_exception=True)
def create_quiz_view(request):
    if request.method == "POST": 
        question_form_set = modelformset_factory(Question, fields=('title', 'text',), extra=1)
        answer_form_set = modelformset_factory(Answer, fields=('text', 'is_correct'), extra=4, max_num=8)
        
        formset_question = question_form_set(request.POST, queryset=Question.objects.none(), prefix="questions")
        formset_answer = answer_form_set(request.POST, queryset=Answer.objects.none(), prefix="answers")
        form = QuizCreateForm(request.POST or None)

        context = {
            'formset_question': formset_question,
            'formset_answer': formset_answer,
            'form': form,
        }
        if all([form.is_valid(), formset_question.is_valid(), formset_answer.is_valid()]):
            post_form = form.save(commit=False)
            post_form_question = formset_question.save(commit=False)
            post_form.author = request.user
            post_form_answer = formset_answer.save(commit=False)
            post_form.save()
            for question in post_form_question:
                for answer in post_form_answer:
                    print(answer)
                print("$")
                # question.quiz = post_form
                # question.save()
                # if post_form_question.index(question) <= 0:
                #     print(question)
                #     for answer in post_form_answer:
                #         answer.quiz = post_form
                #         answer.question = question
                #         answer.save()
                # else:
                #     print(question)
                #     for answer in post_form_answer:
                #         try:
                #             print(answer.question)
                #         except:
                #             answer.quiz = post_form
                #             answer.question = question
                #             answer.save()
            # for question in post_form_question:
            #     question.quiz = post_form
            #     question.save()
            # print(post_form_answer)
            # for answer in post_form_answer:
            #     answer.quiz = post_form
            #     answer.question = post_form_question[0]
            #     answer.save()


 
    
            # post_form_question.quiz = post_form
            # post_form_answer.quiz = post_form
            # post_form_answer.question = post_form_question
        #     post = form.save(commit=False)
        #     post.author = request.user
        #     post.save()
        #     users = form.cleaned_data['created_for']

        #     post_parent = formset_question.save(commit=False)
        #     post_parent.quiz = post
        #     post_parent.type = "radio"
        #     post_parent.save()

            
        #     children = formset_answer.save(commit=False)
        #     for child in children:
        #         child.quiz = post
        #         child.question = post_parent
        #         child.save()

        #     quiz = Quiz.objects.get(id=form.instance.id)
        #     for user in users:
        #         user = User.objects.get(username=user)
        #         Attempts.objects.create(quiz=quiz, user=user, number=form.cleaned_data['attempts'])

    else:
        question_form_set = modelformset_factory(Question, fields=('title', 'text'), extra=1)
        answer_form_set = modelformset_factory(Answer, fields=('text', 'is_correct'), extra=4, max_num=8)
        
        formset_question = question_form_set(request.GET or None, queryset=Question.objects.none(), prefix="questions")
        formset_answer = answer_form_set(request.GET or None, queryset=Answer.objects.none(), prefix="answers")
        form = QuizCreateForm(request.GET or None)

        context = {
            'formset_question': formset_question,
            'formset_answer': formset_answer,
            'form': form,
        }
    return render(request, 'quizes/quiz_create.html', context)
