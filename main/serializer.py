from rest_framework import serializers
from users.models import *
from users.serializers import DoctorLiveSerializer
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
