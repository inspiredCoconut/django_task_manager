# Generated by Django 5.2.1 on 2025-05-12 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
