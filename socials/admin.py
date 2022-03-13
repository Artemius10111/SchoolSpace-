from django.contrib import admin
from .models import (
    LikePost,
    Post,
    Comment,
    HashTag, 
)


class CommentInline(admin.TabularInline):
    model = Comment

class HashTagInline(admin.TabularInline):
    model = HashTag


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline, HashTagInline]



admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
admin.site.register(HashTag)
admin.site.register(LikePost)