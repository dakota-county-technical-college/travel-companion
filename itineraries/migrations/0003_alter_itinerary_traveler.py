# Generated by Django 5.0.1 on 2024-03-16 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraries', '0002_alter_traveler_options_traveler_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerary',
            name='traveler',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='itineraries.traveler'),
        ),
    ]
