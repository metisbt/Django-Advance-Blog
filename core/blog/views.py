from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from .models import Post
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView
from .forms import PostForm

# Function Base View Show a template
'''
def indexView(request):
    """
    a function based view to show index page
    """
    return render(request, 'index.html')
'''

class IndexView(TemplateView):
    '''
    a class based view to show index page
    '''
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.all()
        return context
    
''' FBV for redirect
from django.shortcuts import redirect
def redirectToMaktab(request):
    return redirect('http://maktabkhooneh.com')

'''

class RedirectToMaktab(RedirectView):
    url = 'https://maktabkhooneh.com'

class PostListView(ListView):
    # get objects in different ways
    """
    model = Post
    queryset = Post.objects.all()
    """

    def get_queryset(self):
        posts = Post.objects.filter(status=True)
        return posts

    # change name object_list to posts for templates
    context_object_name = 'posts'

    # for paginate
    paginate_by = 2

class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        posts = Post.objects.filter(status=True)
        return posts

    # change name object_list to posts for templates
    context_object_name = 'posts'

    # for paginate
    paginate_by = 2

# With FormView
'''
class PostCreateView(FormView):
    template_name = "postform.html"
    form_class = PostForm
    success_url = "/blog/post/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
'''

# With CreateView
class PostCreateView(CreateView):
    model = Post
    # fields = ['author', 'title', 'content', 'status', 'category', 'published_date']
    form_class = PostForm
    success_url = '/blog/post/'

    def form_valid(self, form):
        '''
        get user id and save before sending
        '''
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostEditView(UpdateView):
    model = Post
    form_class = PostForm
    success_url = '/blog/post/'

class PostDeleteView(DeleteView):
    model = Post
    success_url = '/blog/post/'
