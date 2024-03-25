# Generated by Django 5.0.1 on 2024-03-16 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itineraries', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='traveler',
            options={'ordering': ['user__first_name', 'user__last_name']},
        ),
        migrations.AddField(
            model_name='traveler',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]