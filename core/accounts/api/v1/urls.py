from django.urls import path, include
from . import views
from rest_framework.authtoken import views


app_name = 'ap-v1'

urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(),name='registration'),
    path('token/login', views.obtain_auth_token.as_view(),name='token-login'),
    # change password
    # reset password
    # login token
    # login jwt
]

