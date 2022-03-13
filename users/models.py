
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.urls.base import reverse
from django.utils.translation import deactivate, ugettext_lazy as _
from config import settings
from django.contrib.auth import get_user_model
import uuid


# CUSTOM_GROUP
##############################################################################################################################

class Custom_Group(Group):
    pass


##############################################################################################################################


# ROLES
##############################################################################################################################

class Roles(Custom_Group):
    class Meta:
        verbose_name = _('Role')

#############################################################################################################################


# USER
#############################################################################################################################

class User(AbstractUser):
    CHOICES = (
        ('user', 'user'),
        ('master', 'master'),
        ('admin', 'admin'),
        ('super_admin', 'super_admin')
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.PositiveSmallIntegerField(null=True)
    role = models.CharField(choices=CHOICES, max_length=11, blank=True) 
    follower_of = models.ManyToManyField("self", related_name="folower_of")  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='images/pic_user/')

    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self):
        return reverse("user_detail", args=[str(self.id)])
    

###########################################################################################################################


# STUDY_GROUP
###########################################################################################################################

class Study_Group(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey('School', on_delete=models.CASCADE, blank=True, null=True)
    users = models.ManyToManyField("users.User")
    creation_data = models.DateTimeField(auto_now_add=True, editable=False)


    class Meta:
        verbose_name = _("Study groups")
        verbose_name_plural = _("Study groups")

    def __str__(self):
        return f'{self.title}'

    
###########################################################################################################################


# SCHOOL
###########################################################################################################################

class School(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    creation_data = models.DateTimeField(auto_now_add=True, editable=False)
    picture = models.ImageField(null=True, upload_to=None, height_field=None, width_field=None, max_length=None, blank=True)
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    school_groups = models.ManyToManyField("Study_Group")
    teachers = models.ManyToManyField("Teacher")
    class Meta:
        verbose_name = _('School')
        verbose_name_plural = _('Schools')

    def __str__(self):
        return self.title


###########################################################################################################################

class Teacher(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    Study_Group = models.OneToOneField('Study_Group', on_delete=models.CASCADE)
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)


    class Meta:
        verbose_name = _("Teacher")
        verbose_name_plural = _("Teachers")

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("Teacher_detail", kwargs={"pk": self.pk})



class FriendRequest(models.Model):
    text_request = models.TextField()
    friend = models.OneToOneField("User", on_delete=models.CASCADE, related_name="friend_will_response")
    author = models.OneToOneField("User", on_delete=models.CASCADE, related_name="author_request_to_friend")

    def __str__(self):
        return f"friend request from {self.author} to {self.friend}"


class Friend(models.Model):
    friend = models.OneToOneField("User", on_delete=models.CASCADE, related_name="friend_requested")
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="friend_responsed")

    def __str__(self):
        return f"{self.user} is frined of {self.friend}"

class Subscription(models.Model):
    user_to = models.OneToOneField("User", on_delete=models.CASCADE, related_name="subscribe_to_user")
    user_from = models.OneToOneField("User", on_delete=models.CASCADE, related_name="subscriber")

    def __str__(self):
        return f"{self.user_from} is subscriber of {self.user_to}"

