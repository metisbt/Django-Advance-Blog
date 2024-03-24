from django.urls import path
from blog import views
from django.views.generic.base import RedirectView

app_name = 'blog'

urlpatterns = [
    path('fbv-index',views.indexView, name='fbv-test'),
    path("cbv-index", views.IndexView.as_view(), name='cbv-index'),
    # path(
    #     "go-to-django/",
    #     RedirectView.as_view(url="https://www.djangoproject.com/"),
    #     name="go-to-django",
    # ),
    path(
        "go-to-index/",
        RedirectView.as_view(pattern_name="blog:index"),
        name="redirect-to-index",
    ),
]