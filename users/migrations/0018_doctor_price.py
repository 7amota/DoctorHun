# Generated by Django 4.1.7 on 2023-03-23 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_ratingsystem'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='price',
            field=models.IntegerField(blank=True, max_length=150, null=True),
        ),
    ]
