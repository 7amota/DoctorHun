# Generated by Django 4.1.7 on 2023-03-23 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_doctor_avg_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='avg_rating',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
            preserve_default=False,
        ),
    ]