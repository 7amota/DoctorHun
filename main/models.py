from django.db import models
from users.models import User, Doctor
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointment_user')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointment_doctor')
    notes = models.CharField(max_length=150, null=True, blank=True)
