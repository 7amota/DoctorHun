# Generated by Django 4.1.7 on 2023-03-25 14:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_remove_doctor_is_liked_remove_doctor_likes_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorlike',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
