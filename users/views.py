import datetime
import jwt

from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _


from rest_framework import status, serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from users.mixins import ApiAuthMixin, PublicApiMixin
from .models import User
from .serializers import UserSerializer, PasswordChangeSerializer

User = get_user_model()

# Create your views here.
class ResisterView(PublicApiMixin, APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




class LoginView(PublicApiMixin, APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        if (email is None) or (password is None):
            return Response({
                "message": "email,password required"
            }, status=status.HTTP_400_BAD_REQUEST)

        '''
        email은 유니크한 값이기 때문에 email 값으로 필터
        '''
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({
                "message": "email is wrong"
            }, status=status.HTTP_403_FORBIDDEN)

        if not user.check_password(password):
            return Response({
                "message": "password is wrong"
            }, status=status.HTTP_403_FORBIDDEN)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True, samesite=None, secure=True)
        response.data = {
            'jwt': token,
            'username': user.name,
        }
        # print(response.cookies)
        return response


class UserView(PublicApiMixin, APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(_('Unauthenticated!'))

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(_('Unauthenticated, token is expired!'))

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


    def put(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed(_('Unauthenticated!'))

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(_('Unauthenticated, token is expired!'))

        user = User.objects.filter(id=payload['id']).first()

        old_password = request.data['oldpassword']
        if not check_password(old_password, user.password):
            raise serializers.ValidationError(
                _("passwords do not match")
            )

        serializer = PasswordChangeSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

        validated_data = serializer.validated_data
        serializer.update(user=user, validated_data=validated_data)
        return Response({
            "message": "Change password success"
        }, status=status.HTTP_200_OK)


class LogoutView(PublicApiMixin, APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout success'
        }
        return response