# Generated by Django 4.1.7 on 2023-03-28 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0027_remove_doctorlike_likes_doctor_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doctor',
            old_name='avg_rating',
            new_name='avgRating',
        ),
        migrations.RenameField(
            model_name='doctor',
            old_name='certificate_image',
            new_name='certificateImage',
        ),
        migrations.RenameField(
            model_name='doctor',
            old_name='is_live',
            new_name='isLive',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='date_birth',
            new_name='dateBirth',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_doctor',
            new_name='isDoctor',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phone_number',
            new_name='phoneNumber',
        ),
        migrations.AddField(
            model_name='doctor',
            name='yearsExpirinces',
            field=models.IntegerField(blank=True, max_length=150, null=True),
        ),
        migrations.DeleteModel(
            name='DoctorLike',
        ),
    ]
