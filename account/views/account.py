from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.core.exceptions import ValidationError
from rest_framework import viewsets
from rest_framework import permissions, authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from ..models import Profile
from ..serializers.account import AccountSerializer

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from ..tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string, get_template
from django.utils.encoding import force_bytes
from django.conf import settings

class ApiLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
        except:
            return Response({'success':False,'message':'User not found'},status=status.HTTP_404_NOT_FOUND)
        if user.is_active:
            return Response({'success':True,'token':token.key, 'nextUrl':'/account/home/'},status=status.HTTP_200_OK)

        return Response({'success':False,'message':'User not verified'},status=status.HTTP_404_NOT_FOUND)

class ObtainAccount(viewsets.ViewSet):
    authentication_classes = [authentication.TokenAuthentication]

    def register(self, request):
        try:
            email=request.data['email']
            username=request.data['username']
            if User.objects.filter(email = email).first():
                return Response({'message':'email already registered'},status=status.HTTP_200_OK)

            if User.objects.filter(username = username).first():
                return Response({'message':'this username already registered'},status=status.HTTP_200_OK)
                
            serializer = AccountSerializer(data=request.data,
                                           context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            profile=Profile.objects.create(user=user)
            site = get_current_site(request)
            print("mail sendinng")
            mail_subject = "Confirmation message"
            message = render_to_string('account/activate.html', {
                "user": user,
                'domain': site.domain,
                'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })
            to_email = email
            to_list = [to_email]
            from_email = settings.EMAIL_HOST_USER
            send_mail(mail_subject, message, from_email, to_list, fail_silently=True)
            # print("mail sent")
            return Response({'token':token.key,'message':'user created successfully'},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e),'message':'user no created'},status=status.HTTP_404_NOT_FOUND)

    def activate(self,request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(id=uid)
        except(TypeError, ValueError):
            user = None
        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'success':True,'message':'user activated successfully'},status=status.HTTP_200_OK)
        else:
            return Response({'success':False,'message':'user no created'},status=status.HTTP_404_NOT_FOUND)

    def logout(self, request, format=None):
        try:
            auth = request.META.get('HTTP_AUTHORIZATION')
            _, token = auth.split()
            user = Token.objects.get(key=token).user
            user.auth_token.delete()
            return Response({'success':True, 'message':'logout successfully','nextUrl':'/account/login/'},status=status.HTTP_200_OK)
        except:
            return Response({'success':False,'message':'User not found'},status=status.HTTP_404_NOT_FOUND)

