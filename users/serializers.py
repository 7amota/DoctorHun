from .models import *
from rest_framework import serializers
from rest_framework.validators import ValidationError
class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username" , "password","phoneNumber", "image" , "location" , "dateBirth",'isDoctor' ]
        
    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()


        return user

class UserIISerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username" , "password","phoneNumber", "image" , "location" , "dateBirth" ]

class MainPageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'image']


class DoctorLiveSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    isLiked = serializers.SerializerMethodField()
    class Meta:
        model = Doctor
        fields = ['id','username','image' ,'isLiked', 'isLive' , 'views', 'avgRating', 'price', 'specialist']
    
    def get_price(self,obj):
        return obj.price if obj.price != None else 0
    def get_isLiked(self,obj):
        user = self.context.get('user')
        return True if user in obj.likes.all() else False



