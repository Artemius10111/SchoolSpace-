from django.conf.urls import url
from django.urls import path, include 
from . import views

urlpatterns = [
    path('lessons/', views.LessonListView.as_view(), name="lesson_list"),
    path('add_lesson/', views.lesson_add_view, name="add_lesson"),
    path('<uuid:pk>/lesson/', views.lesson_view, name="lesson_description"),
    path('school/', views.school_view, name="school"),
]
