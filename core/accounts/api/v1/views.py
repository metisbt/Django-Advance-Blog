from rest_framework import generics
from .serializers import RegistrationSerializer, CustomAuthTokenSerializer, ChangePasswordApiSerializer, ProfileSerializer, TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from accounts.models import Profile
from django.shortcuts import get_object_or_404
# for JWT
from rest_framework_simplejwt.views import TokenObtainPairView
# for send simple emails
# from django.core.mail import send_mail
# for send customize emails
from mail_templated import send_mail
# customize email send with treading
from mail_templated import EmailMessage
from ..utils import EmailThread
# for generate token manually
from rest_framework_simplejwt.tokens import RefreshToken
# for decode simplejwt token
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.conf import settings



User = get_user_model()

# APIView doesn't need serialization but GenericViews need it


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data['email']
            data = {
                'email':email,
            }
            # generate token manually
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            # customize email send with treading
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', to=[email])
            EmailThread(email_obj).start()
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    

class CustomObtainAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class CustomDiscardAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ChangePasswordApiView(generics.GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordApiSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    
    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'detail':'Password updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

# for JWT
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

# send email
'''class TestEmailSend(generics.GenericAPIView):

    def post(self, request, *args, **kwargs):
        # simple send email
        """send_mail(
            "Subject here",
            "Here is the message.",
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,
        )"""
        # customize email send
        # send_mail('email/hello.tpl', {'name': 'mahdi'}, 'admin@admin.com', ['test@test.com'])

        # generate token manually
        self.email = 'metisbt@gmail.com'
        user_obj = get_object_or_404(User, email=self.email)
        token = self.get_tokens_for_user(user_obj)

        # customize email send with treading
        email_obj = EmailMessage('email/hello.tpl', {'token': token}, 'admin@admin.com', to=[self.email])
        EmailThread(email_obj).start()

        return Response('sent email')
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)'''

# for activation token with email send in registration
class ActivationApiView(APIView):

    def get(self, request, token, *args, **kwargs):
        # decode -> user id
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = token.get('user_id')
        # if token expired
        except ExpiredSignatureError:
            return Response({'details':'toke has been expired'}, status=status.HTTP_400_BAD_REQUEST)
        # if token not valid
        except InvalidSignatureError:
            return Response({'details':'toke is not valid'}, status=status.HTTP_400_BAD_REQUEST)
        
        # object user
        user_obj = User.objects.get(pk = user_id)
        if user_obj.is_verified:
             return Response({'detail':'your account has already verified'}, status=status.HTTP_200_OK)
        # is_verified -> True
        user_obj.is_verified = True
        user_obj.save()
        # valid response ok
        return Response({'detail':'your account have been verified and activated successfully'},status=status.HTTP_200_OK)

# for resend activation token
class ActivationResendApiView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if email:
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            # customize email send with treading
            email_obj = EmailMessage('email/activation_email.tpl', {'token': token}, 'admin@admin.com', to=[email])
            EmailThread(email_obj).start()
            return Response({'detail':'user activation resend successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail':'invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)