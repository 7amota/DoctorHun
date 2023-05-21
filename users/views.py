from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMessage
from django.db.models import Sum, Count , Avg
from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.utils import json

from .models import *
from .serializers import *
from .logs import log

import random
import requests




class GoogleView(APIView):
    def post(self, request):
        payload = {'access_token': request.data.get("token")}  # validate the token
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params=payload)
        data = json.loads(r.text)

        if 'error' in data:
            content = {'message': 'wrong google token / this google token is already expired.'}
            return Response(content)

        # create user if not exist
        try:
            user = User.objects.get(email=data['email'])
            serializer= UserSerializer(user)
            print(serializer.instance)
            token, _ = Token.objects.get_or_create(user=serializer.instance)
            response = {
                'status':1,
                'message':"user Logged in",
                'data':serializer.data,
                'token':token.key
            }
            return Response(response)
        except:
            userf = User.objects.create_user(email=data['email'], password=make_password(BaseUserManager().make_random_password()) , username='lol')
            serializef= UserSerializer(userf)
            tokenf, _ = Token.objects.get_or_create(user=serializef.instance)
            responsef = {
                'status':1,
                'data':serializef.data,
                'token':tokenf.key
            }
            return Response(responsef)






class RegiserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def post(self, request:Request, *args, **kwargs):
        data = request.data
        email = User.objects.filter(email=data['email']).exists()
        if email == False:
            serializer = self.serializer_class(data=data, context={"request":request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                token, _ = Token.objects.get_or_create(user=serializer.instance)
                print(serializer.instance)
                res = {
                    "status":1,
                    "message":"Account Created .",
                    "data":serializer.data,
                    "token":token.key

                }
                log(message=res)
                return Response(res , status.HTTP_200_OK)
        else:
            message ={
                'status':0,
                'message':'Email had been used , try another one'
            }
            return Response(message, status.HTTP_200_OK)

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
            log(message=response)

            return Response(data=response, status=status.HTTP_200_OK)

        else:
            try:
                ob = Doctor.objects.get(email=email)
                tokensl, created = Token.objects.get_or_create(user=ob)
                responsem = {
                "status":1,
                "message": "Login Successfull",
                "id": tokensl.user_id,
                "token": tokensl.key
            }

                log(message=responsem)
                return Response(
                    responsem,status.HTTP_200_OK

                )



            except:
                return Response({
                "status":0,
                "message": "Invalid email or password"

                }, status.HTTP_404_NOT_FOUND)


class LogoutView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        token = Token.objects.get(user=user)
        try:
            token.delete()
            res = {
                "status":1,
                "message":"user gone ): "
            }
            return Response(res,status.HTTP_410_GONE)
        except:
            mes = {
                "status":0,
                "message":"some thing went wrong like there is no token for this user"
            }
            log(message=mes)

            return Response(mes , status.HTTP_400_BAD_REQUEST)

class UpdateUser(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserIISerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        data = self.serializer_class(user)

        return Response(data.data , status.HTTP_200_OK)
    def put(self, request, *args, **kwargs):
        try:
            data=self.serializer_class(request.user, data=request.data, partial=True, context={
                "request":request
            })
            if data.is_valid(raise_exception=True):
                data.save()

            res = {
                "status":1,
                "data":data.data
            }
            return Response(res, status.HTTP_200_OK)
        except:
            mes = {
                "status":0,
                "message":"some thing went wrong like token is not found or data is not valid"
            }
            return Response(mes, status.HTTP_400_BAD_REQUEST)



class ResetRequest(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserIISerializer
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            email = EmailMessage('DoctorHunt Reset Password Request', f'your otp is {user.otp}', to=[user.email])
            email.send()
            message = {
                "status":1,
                "otp":user.otp,

                'message': 'Done .'}
            log(message=message)

            return Response(message, status=status.HTTP_200_OK)
        else:
            message = {
                "status":0,
                'message': 'Error like the email is not valid .'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)



class ResetPassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserIISerializer
    def put(self, request:Request, *args, **kwargs):
        otp = request.data['otp']
        new_password = request.data['new_password']
        user = User.objects.get(otp=otp)
        if otp == user.otp:
            user.set_password(new_password)
            user.save()

            number_list = [x for x in range(10)]  # Use of list comprehension
            code_items_for_otp = []

            for i in range(4):
                num = random.choice(number_list)
                code_items_for_otp.append(num)

            code_string = "".join(str(item)for item in code_items_for_otp)  # list comprehension again
            # A six digit random number from the list will be saved in top field
            user.otp = code_string
            user.save()
            mes = {
                "status":1,
                "message":"user reseted password successfully"
            }
            log(message=mes)

            return Response(mes)
        else:
            les = {
                "status":0,
                "message":"otp is not valid "
            }
            log(message=les)

            return Response(les)


class CreateDoc(generics.CreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorCreationClass
    def post(self, request:Request, *args, **kwargs):
        data = request.data
        email = User.objects.filter(email=data['email']).exists()
        if email == False:
            serializer = self.serializer_class(data=data, context={"request":request})
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                token, _ = Token.objects.get_or_create(user=serializer.instance)
                print(serializer.instance)
                res = {
                    "status":1,
                    "message":"Account Created .",
                    "data":serializer.data,
                    "token":token.key

                }
                log(message=res)
                return Response(res , status.HTTP_200_OK)
        else:
            message ={
                'status':0,
                'message':'Email had been used , try another one'
            }
            return Response(message, status.HTTP_200_OK)

class Statistics(generics.ListAPIView):
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permissions_classess = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        doctorAccounts = Doctor.objects.all()
        livesDoctors = Doctor.objects.filter(isLive = True).count()
        DViews = DocViews.objects.all().count()
        DocSpecialist = Doctor.objects.values_list('specialist')
        liks=  Doctor.objects.filter(pk=3).values('likes')
        
        print(liks)
        lis = []
        for i in DocSpecialist:
            for x in i:
                if x not in lis:
                    lis.append(x)
        

        res = {
            'accountsCount': len(users),
            'usersAccounts': len(users) - len(doctorAccounts),
            'doctorAccounts': len(doctorAccounts),
            'livesDoctors':livesDoctors,
            'SumOfDoctorsViews':DViews,
            "ExistDocSpecialist":lis, # specialist is loop 

        }
        return Response(res,status.HTTP_200_OK)
