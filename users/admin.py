from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.site_title = "DoctorHunt"
admin.site.site_header = "DoctorHunt"
admin.site.index_title = "DoctorHunt Administration"