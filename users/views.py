import django
from django import template
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.shortcuts import redirect, render
from django.urls.base import reverse, reverse_lazy
from django.views import generic
from .models import School, User
from .forms import CustomUserChangeForm, CustomUserCreationForm, SchoolCreateForm
from django.contrib.auth.models import Group
from django.contrib.auth import views as django_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template import RequestContext
import os
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.
class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    model = User
    success_url = reverse_lazy("SignUp")
    template_name = 'account/registration.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile', request.user.id)
        else:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                group_name = form.cleaned_data['role']
                group = Group.objects.get(name=f'{group_name}s')
                user.groups.add(group)
                print(f'{user.username} was added to {group_name}s')
                return redirect('login')
            else:
                form = UserCreationForm()
                return redirect('login')
    
            


class LoginView(django_views.LoginView):
    template_name = 'account/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile', request.user.id)
        else:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form})


class PasswordChangeView(django_views.PasswordChangeView):
    template_name = 'account/password_change.html'
    success_url = reverse_lazy('password_change')

class PasswordChangeDoneView(django_views.PasswordChangeDoneView):
    template_name = 'account/password_change_done.html'
    success_url = reverse_lazy('change_password_done')


class PasswordResetView(django_views.PasswordResetView):
    template_name = 'account/password_reset.html'
    success_url = reverse_lazy('password_reset')
    

class LogoutView(django_views.LogoutView):
    template_name = 'account/logout.html'

class ProfileView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    login_url = 'users/login'
    redirect_field_name = 'login'
    template_name = 'account/profile.html'
    success_url = 'profile'
    form_class = CustomUserChangeForm
    model = User
    success_message = "Your profile was successfully updated"


def profile_view(request, pk):
    user = User.objects.get(id=pk)
    if user == request.user:
        if request.method == "POST":
            form = CustomUserChangeForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save(commit=False)
        else:
            form = CustomUserChangeForm(request.GET or None, instance=request.user)
        context = {
            'profile_edit': 'profile_edit',
            'form': form
        }
        return render(request, 'account/profile.html', context)
    else:
        context = {
            'profile_view': 'profile_view',
            'user_profile': user,
        }
        return render(request, 'account/profile.html', context)
    
class SchoolCreateView(PermissionRequiredMixin ,CreateView):
    success_url = reverse_lazy('school_create')
    permission_required = 'school_create'
    template_name = 'account/school_create.html'
    model = School
    form_class  = SchoolCreateForm