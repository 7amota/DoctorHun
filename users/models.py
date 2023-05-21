from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

import random
from .specialist import specialties

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)

        




class User(AbstractUser):
    choices_gender = (
        ("male","male"),
        ("female","female")
    )
    email = models.EmailField(max_length=80, unique=True)
    image = models.ImageField(upload_to='Photos/%y/%m/%d',null=True , blank=True)
    username = models.CharField(max_length=45)
    phoneNumber = models.IntegerField(null=True , blank=True)
    dateBirth = models.DateField(null=True , blank=True)
    location = models.TextField(null=True , blank=True)
    gender = models.TextField(null=True , blank=True , choices=choices_gender)
    isDoctor = models.BooleanField(null=True , blank=True, default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    otp = models.CharField(max_length=6, null=True, blank=True)
    qrcode = models.ImageField(upload_to='Photos/%y/%m/%d',null=True , blank=True)
    
    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)] 
        code_items_for_otp = []
        
        for i in range(4):
            num = random.choice(number_list)
            code_items_for_otp.append(num)

        code_string = "".join(str(item)for item in code_items_for_otp)
        self.otp = code_string
        super().save(*args, **kwargs)

class Doctor(User):
    specialist = models.CharField(max_length=50,choices=specialties, null=True , blank=True)
    certificateImage = models.ImageField(upload_to='Photos/%y/%m/%d',null=True , blank=True)
    isLive = models.BooleanField(default=False , null=True  , blank=True)
    views = models.IntegerField(null=True  , blank=True)
    price = models.IntegerField(null=True , blank=True)
    avgRating = models.DecimalField(null=True , blank=True,max_digits=5, decimal_places=2)
    likes = models.ManyToManyField(User, blank=True, related_name='doctorlikes')
    yearsExpirinces = models.IntegerField(null=True,blank=True)
    class Meta:
        verbose_name = 'Doctors'
   

class DocViews(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name='user')
    doc = models.ForeignKey(Doctor, on_delete=models.CASCADE , related_name='doc')
    class Meta:
        unique_together = ('user','doc')
        index_together = ("user" , 'doc')

        

class RatingSystem(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='userrate')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='ratedoctor')
    rate= models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    class Meta:
        unique_together = ('user','doctor')
        index_together = ('user','doctor')
















