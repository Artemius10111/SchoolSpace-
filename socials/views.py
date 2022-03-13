from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q
from socials.models import Post, Comment
from .forms import CommentCreateForm, PostCreateForm, PostUpdateForm
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# Create your views here.
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "socials/post_create.html"
    success_url = reverse_lazy('post_create')
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()

def create_post_view(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return render(request, 'socials/post_create.html', {'form': form})
    else: 
        form = PostCreateForm()
        return render(request, 'socials/post_create.html', {'form': form})

class Search(ListView):
    template_name = 'socials/post_search.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        try:
            q = self.request.GET.get('q').capitalize()
        except AttributeError:
            return None
        return Post.objects.filter(title__icontains=q)

    def get_context_data(self, *args, **kwargs):
        try: 
            context = super().get_context_data(*args, **kwargs)
        except:
            return None
        context["q"] = f'q={self.request.GET.get("q")}&'
        context["searched"] =  self.request.GET.get("q")
        return context


def post_detail_view(request, pk):
    post = Post.objects.get(id=pk)
    comments = list(reversed(Comment.objects.filter(post=post)))
    num_of_comments = len(comments)
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            print('valid')
            post_form = form.save(commit=False)
            post_form.author = request.user
            post_form.post = post
            post_form.save()
    else:
        form = CommentCreateForm()
    return render(request, 'socials/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'page_obj': page_obj, "num_of_comments": num_of_comments})


def view_your_posts(request):
    posts = Post.objects.filter(author=request.user)
    context = {
        "posts": posts,
    }
    return render(request, 'socials/your_posts.html', context)

def like_post(request, id):
    return redirect('post_detail')