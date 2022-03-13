
from django.urls import path
from .views import (
    QuizListView,
    ResultsListView,
    UpdateQuizView,
    create_quiz_view,
    quiz_action_view,
    quiz_view,
    quiz_data_view,
    quiz_save_view,
    results_detail_view,
    )

urlpatterns = [
    path('', QuizListView.as_view(), name='quiz_list'),
    path('<uuid:pk>/quiz_description/', quiz_view, name='quiz_description'),
    path('<uuid:pk>/data/', quiz_data_view, name='quiz_data'),
    path('<uuid:pk>/action/', quiz_action_view, name='quiz_action'),
    path('<uuid:pk>/save/', quiz_save_view, name='quiz_save'),
    path('create/', create_quiz_view, name="quiz_create"), 
    path('<uuid:pk>/update/', UpdateQuizView.as_view(), name='quiz_update'),
    path('results/', ResultsListView.as_view(), name='quiz_results',),
    path('results/<uuid:pk>/', results_detail_view, name='result_detail'),
]
