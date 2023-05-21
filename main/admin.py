from django.contrib import admin
from users.models import *
from .models import Appointment
# Register your models here.
admin.site.register(RatingSystem)
admin.site.register(DocViews)
admin.site.register(Appointment)