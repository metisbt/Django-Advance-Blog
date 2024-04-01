from django.urls import path, include
from . import views
# from rest_framework.authtoken import views
# for JWT
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )


app_name = 'ap-v1'

urlpatterns = [
    # registration
    path('registration/', views.RegistrationApiView.as_view(),name='registration'),
    # change password
    # reset password
    # login token
    path('token/login/', views.CustomObtainAuthToken.as_view(),name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(),name='token-logout'),
    # login jwt
    # path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create')
    # path('jwt/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    # path('jwt/verify/', TokenVerifyView.as_view(), name='token-refresh'),
]

