# Generated by Django 4.1.7 on 2023-04-27 20:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0041_alter_image_certificateimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='certificateImage',
            field=models.FileField(blank=True, null=True, upload_to='Photos/%y/%m/%d', validators=[django.core.validators.validate_image_file_extension, django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]