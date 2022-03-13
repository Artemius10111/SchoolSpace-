from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Roles, Study_Group, Subscription, User, School, Teacher, FriendRequest, Friend
from django.contrib.auth.admin import GroupAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.utils.translation import ugettext_lazy as _
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Account settings',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'age',
                    'role'
                ),
            },
        ),
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'age', 'role', 'profile_pic',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ['username', 'role',]

# class FriendRequestInline(admin.TabularInline):
#     model = FriendRequest

# class FriendAdmin(admin.ModelAdmin):
#     inlines = (FriendRequestInline, )
#     model= Friend


admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Roles, GroupAdmin)
admin.site.register(Study_Group)
admin.site.register(School)
admin.site.register(Teacher)
admin.site.register(Subscription)
admin.site.register(FriendRequest)
admin.site.register(Friend)

# admin.site.register(Study)
# Register your models here.
