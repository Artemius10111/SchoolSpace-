from django.db import models
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.utils.translation import ugettext_lazy as _
import uuid 
from config import settings

class Post(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    author = models.ForeignKey('users.user', on_delete=models.CASCADE, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    date = models.DateTimeField(editable=False, auto_now_add=True, null=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(default="Comment", blank=True, max_length=25)
    text = models.TextField()
    post = models.ForeignKey('Post', on_delete=models.CASCADE, blank=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"Comment {self.name} of {self.post} post!"



class HashTag(models.Model):
    name = models.CharField(max_length=100)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _("HashTag")
        verbose_name_plural = _("HashTags")

    def __str__(self):
        return self.name

LIKE_VALUES = (('LIKE', 'LIKE'),
                ('DISLIKE', 'DISLIKE'))

class LikePost(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_VALUES, max_length=7, default="LIKE")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class LikeComment(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    comment = models.ForeignKey("Comment", on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_VALUES, max_length=7, default="LIKE")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)