from django.urls import path, include

from users.forms import SchoolCreateForm
from . import views
from django.contrib.auth import views as django_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('registration/', views.SignUpView.as_view(), name="SignUp"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('<uuid:pk>/logout/', views.LogoutView.as_view(), name='logout'),
    path('<uuid:pk>/password_change/', views.PasswordChangeView.as_view(), name="password_change"),
    path('<uuid:pk>/password_change/done', views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('<uuid:pk>/profile', views.profile_view, name="profile"),
    path('<uuid:pk>/password_reset/', views.PasswordResetView.as_view(), name="password_reset"),
    path('school_create/', views.SchoolCreateView.as_view(), name='school_create' ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
