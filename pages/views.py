from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.template import RequestContext

from users.models import User
# Create your views here.
def home_page_view(request):
    return render(request, 'pages/home.html')

class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    success_url = reverse_lazy('about')

class StartPageView(TemplateView):
    template_name = 'pages/start.html'
    success_url = reverse_lazy('start')

class CallSupportView(TemplateView):
    template_name = 'pages/call_support.html'
    success_url = reverse_lazy('call_support')

def page_not_found_view(request, exception):
    return render(request, 'pages/404.html', status=404)

def page_forbidden_403_view(request, exception):
    return render(request, 'pages/403.html', status=403)

#e[uogwegjw]