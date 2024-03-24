from django.urls import path
from blog import views
from django.views.generic.base import RedirectView

app_name = 'blog'

urlpatterns = [
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
    path(
        "go-to-maktabkhooneh/",
        views.RedirectToMaktab.as_view(),
        name="redirect-to-maktabkhooneh",
    ),
    # for PostList url must like this with '/' at the end
    path('post/', views.PostList.as_view(), name="post-list"),
]