# Generated by Django 4.1.7 on 2023-02-27 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='specialist',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
