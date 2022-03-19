from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from rest_framework.authtoken.models import Token


class ExampleAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Credentials string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = Token.objects.get(token=auth[1])
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such token')

        return token
