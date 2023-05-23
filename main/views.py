from django.db import connection

from rest_framework import generics , mixins , viewsets, status 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny , IsAdminUser , IsAuthenticated
from rest_framework.response import Response
from rest_framework import filters

from users.serializers import *
from users.models import *
from .permissions import IsDoctor, CustomPermissionsForAppointements, CheckAuthor
from .serializers import *
from users.logs import log


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
        doc = Doctor.objects.get(pk=request.data.get('doctorId'))
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
        doctorid = request.data.get('doctorId')
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
        doctorid = request.data.get('doctorId')
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
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        print(f"Queries Count {len(connection.queries)}")
        return response
    
    def get(self, request, *args, **kwargs):
        user = request.user
        doctor = Doctor.objects
        userData = UserSerializer(user, context={'request':request})
        doc = doctor.filter(isLive=True)
        liveData = DoctorLiveSerializer(doc , many=True, context={'user':request.user, 'request':request})
        pouplarDoctor = doctor.order_by("-views")
        pouplarDoctorData = DoctorLiveSerializer(pouplarDoctor, many=True, context={'user':request.user, 'request':request})
        featureDoctors = DocViews.objects.select_related('user').filter(user=user)
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields= ['^username']

class Appointemtns(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        doctor_id = request.data.get('doctor')
        doctor = Doctor.objects.get(pk=doctor_id)
        serializer = self.serializer_class(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save(doctor=doctor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class AppointemntsRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [CheckAuthor, IsAuthenticated]
    lookup_field = 'id'
