from django.urls import path
from .views import Search, create_post_view, post_detail_view, view_your_posts, like_post


urlpatterns = [
    path('create_post/', create_post_view, name='post_create'),
    path('search/', Search.as_view(), name='post_search'),
    path('<uuid:pk>/post_detail', post_detail_view, name='post_detail'),
    path('your_posts/', view_your_posts, name="your_posts"),
    path('like_post/', like_post, name="like_post"),
]
