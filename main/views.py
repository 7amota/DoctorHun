from users.serializers import *
from users.models import *
from rest_framework import generics , mixins , viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated
from .permissions import IsDoctor
from rest_framework.response import Response
from .serializer import *
import requests
from rest_framework import filters
def log(message):
    bot_token = "6107600815:AAFIafRsJCNiw4nHBfUx7RXepZ7eujykhSw"
    groub_id = 1409161603
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={groub_id}&parse_mode=Markdown&text={message}"
    requests.get(url)


class LiveDoctor(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsDoctor]
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            try:
                doctor = Doctor.objects.get(email=user , isLive=True)
                doctor.isLive = False
                doctor.save()
                date = DoctorLiveSerializer(doctor)
                message = {
                    'status':1,
                    'data' : date.data
                }
                return Response(message ,status.HTTP_200_OK)
            except:
                doc = Doctor.objects.get(email=user ,is_live=False)
                doc.isLive = True
                doc.save()
                data = DoctorLiveSerializer(doc)
                messag = {
                    'status':1,
                    'data' : data.data
                }
                log(message=messag)
                return Response(messag ,status.HTTP_200_OK)

        except:
            message = {
                'status':0,
                'message':'some thing went wrong like the user is not doctor );'
            }
            log(message=message)
            return Response(message , status.HTTP_400_BAD_REQUEST)

class DoctroView(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        doc = Doctor.objects.get(pk=request.data.get('doctor_id'))
        user = request.user
        try:

            get = DocViews.objects.get(doc=doc,user=user)
        
            message = {
                    'status':0,
                    "message":'smoe thing wrong like user has already seen the doctor ):'
                }
            log(message=message)

            return Response(message ,status.HTTP_400_BAD_REQUEST)                
                    

        except:
            view = DocViews.objects.create(user=user , doc=doc, view=1)
            doc.save()
            ser = ViewsSerializerII(view)
            messag = {
                'status':1,
                "data":ser.data
            }
            log(message=messag)

            return Response(messag, status.HTTP_200_OK)


class Rate(generics.CreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user
        doctorid = request.data.get('doctorid')
        doctor = Doctor.objects.get(pk=doctorid)
        try:
           rata = RatingSystem.objects.get(user=user , doctor=doctor)
           rata.rate = request.data.get('stars')
           rata.save()
           doctor.save()
           dat = RateSerializer(rata)
           message = {
               'status':1,
               'message':"updated successfully",
               'data':dat.data
           }
           log(message=message)

           return Response(message, status.HTTP_200_OK)
        except:
            rate = RatingSystem.objects.create(user=user,doctor=doctor,rate=request.data.get('stars'))
            doctor.save()
            data = RateSerializer(rate)
            messag={
                'status':1,
                'message':"Rate had been created successfully",
                "data":data.data
            }
            log(message=messag)

            return Response(messag, status.HTTP_200_OK)

class Like(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)
        doctorid = request.data.get('doctorid')
        doctor = Doctor.objects.get(pk=doctorid)
        if user in doctor.likes.all():
            doctor.likes.remove(user)
            doctor.save()
            message = {
                'status':1,
                "isLiked":False
            }
            log(message=message)

            return Response(message, status.HTTP_200_OK)

        else:
            doctor.likes.add(user)
            doctor.save()
            serializer = DoctorLiveSerializer(doctor)
            message = {
                "status":1,
                'isLikde':True,
            }
            log(message=message)

            return Response(message, status.HTTP_200_OK)








class MainPage(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        user = request.user
        doctor = Doctor.objects.all()
        userData = UserSerializer(user)
        doc = doctor.filter(isLive=True)
        liveData = DoctorLiveSerializer(doc , many=True, context={'user':request.user, 'request':request})
        pouplarDoctor = doctor.order_by("-views")
        pouplarDoctorData = DoctorLiveSerializer(pouplarDoctor, many=True, context={'user':request.user, 'request':request})
        featureDoctors = DocViews.objects.filter(user=user)
        featureDoctorSerializer = ViewsSerializer(featureDoctors , many=True, context={'user':request.user, 'request':request} )
        message = {
            'userData':userData.data,
            'livesDoctors':liveData.data,
            'popularDoctors':pouplarDoctorData.data,
            'featureDoctors':featureDoctorSerializer.data,
        }

        return Response(message, status=status.HTTP_200_OK)

class DoctorsList(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorLiveSerializer
    filter_backends = [filters.SearchFilter]
    search_fields= ['^username']
