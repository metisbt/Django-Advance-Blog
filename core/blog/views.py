from typing import Any
from django.shortcuts import render
from django.views.generic.base import TemplateView, RedirectView
from .models import Post

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