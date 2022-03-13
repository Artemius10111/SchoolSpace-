from django.urls import path, include 
from . import views

urlpatterns = [
    path('home', views.home_page_view, name='home'),
    path('about', views.AboutPageView.as_view(), name='about'),
    path('', views.StartPageView.as_view(), name='start'),
    path('call_support', views.CallSupportView.as_view(), name='call_support'),
    
]
