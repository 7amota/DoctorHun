# Generated by Django 4.1.7 on 2023-02-27 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_doctor_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_doctor',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
