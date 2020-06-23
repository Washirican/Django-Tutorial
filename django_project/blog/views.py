from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post


# NOTE (D. Rodriguez 2020-06-22): Home Function
# NOTE (D. Rodriguez 2020-06-22): Using function-based views
def home(request):
    context = {
        'posts': Post.objects.all()
        }
    return render(request, 'blog/home.html', context)


# NOTE (D. Rodriguez 2020-06-22): Using class-based views
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


# NOTE (D. Rodriguez 2020-06-22): Using class-based view conventions to cut
# down on code
class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # NOTE (D. Rodriguez 2020-06-22): Sets author of new post to current user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    # NOTE (D. Rodriguez 2020-06-22): Sets author of new post to current user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
