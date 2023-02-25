from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import *

@api_view(["GET"])
def test(request):
    res = {
        "message":"working"
    }
    return Response("lol", status.HTTP_200_OK)

class RegiserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request:Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token, _ = Token.objects.get_or_create(user=serializer.instance)
        print(serializer.instance)
        res = {
            "status":1,
            "message":"Account Created .",
            "data":serializer.data,
            "token":token.key

        }
        return Response(res , status.HTTP_200_OK)

class LoginView(generics.CreateAPIView):
    serializer_class = AuthTokenSerializer
    def post(self, request: Request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:

            tokens, created = Token.objects.get_or_create(user=user)
            response = {
                "status":1,
                "message": "Login Successfull",
                "id": tokens.user_id,
                "token": tokens.key
            }
            return Response(data=response, status=status.HTTP_200_OK)

        else:
            return Response({
                "status":0,
                "message": "Invalid email or password"
                
                }, status.HTTP_404_NOT_FOUND)




