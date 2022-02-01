import datetime
import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework import status

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from django.utils.translation import gettext_lazy as _


from users.mixins import ApiAuthMixin, PublicApiMixin
from .models import User
from .serializers import UserSerializer


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
            raise AuthenticationFailed(_('User not found!'))

        if not user.check_password(password):
            raise AuthenticationFailed(_('Incorrect password!'))

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
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


class LogoutView(PublicApiMixin, APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout success'
        }
        return response