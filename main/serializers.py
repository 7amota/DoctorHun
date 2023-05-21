from rest_framework import serializers
from users.models import *
from .models import  Appointment
from users.serializers import DoctorLiveSerializer, DoctorCreationClass

class ViewsSerializer(serializers.ModelSerializer):
    doc = DoctorLiveSerializer()
    class Meta:
        model = DocViews
        fields = ['doc']

class ViewsSerializerII(serializers.ModelSerializer):
    class Meta:
        model=DocViews
        fields = ['user','doc','view']

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatingSystem
        fields = ['doctor','user','rate',]

class AppointmentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    doctor = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = ['id','user','doctor','notes']
        extra_kwargs = {'user': {'required': False}}
    

    def create(self, validated_data):
        print(validated_data)
        user = self.context.get('request').user
        doctor = validated_data.get('doctor')
        appoint = Appointment()
        appoint.user = user
        appoint.doctor= doctor
        appoint.notes = validated_data.get('notes',None)
        return appoint
    def get_user(self,obj):
        if obj.user.image:
            return {
                'id':obj.user.pk,
                'username':obj.user.username,
                'phoneNumber':obj.user.phoneNumber,
                'email':obj.user.email,
                'image':obj.user.image.url,
            }
        else:
            return {
                'id':obj.user.pk,
                'username':obj.user.username,
                'phoneNumber':obj.user.phoneNumber,
                'email':obj.user.email,
                'image':None,
            }
    def get_doctor(self,obj):
        if obj.doctor.image:
            return {
                'id':obj.doctor.pk,
                'username':obj.doctor.username,
                'phoneNumber':obj.doctor.phoneNumber,
                'email':obj.doctor.email,
                'image':obj.doctor.image.url,
            }
        else:
            return {
                'id':obj.doctor.pk,
                'username':obj.doctor.username,
                'phoneNumber':obj.doctor.phoneNumber,
                'email':obj.doctor.email,
                'image':None,
            }

    