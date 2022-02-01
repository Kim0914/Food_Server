import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from users.models import User


User = get_user_model()


class SafeJWTAuthentication(BaseAuthentication):
    """
    JWT Authentication
    헤더의 jwt 값을 디코딩해 얻은 user_id 값을 통해서 유저 인증 여부를 판단한다.
    """

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None

        try:
            prefix = authorization_header.split(' ')[0]
            if prefix.lower() != 'jwt':
                raise exceptions.AuthenticationFailed('Token is not jwt')

            access_token = authorization_header.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256']
            )
            # print(payload)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        return self.authenticate_credentials(request, payload['id'])

    def authenticate_credentials(self, request, key):
        user = User.objects.filter(id=key).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')

        # self.enforce_csrf(request)
        return (user, None)


class AdministratorAuthentication(SafeJWTAuthentication):
    def authenticate(self, request):
        return super().authenticate(request)

    def authenticate_credentials(self, request, key):
        user = User.objects.filter(id=key).first()

        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User is inactive')

        if not user.is_superuser:
            raise exceptions.AuthenticationFailed('User is not superuser')

        # self.enforce_csrf(request)

        return (user, None)

