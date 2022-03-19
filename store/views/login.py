from django.contrib.auth import authenticate, login as Login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['POST'])
def login(request):
    user = authenticate(username=request.data["username"], password=request.data["password"])

    if user is not None:
        Login(request._request, user)
        return Response({"token": user.auth_token.key})
    else:
        response = {
            "error": "Invalid credentials"
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
