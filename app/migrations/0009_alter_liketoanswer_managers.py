# Generated by Django 4.1.3 on 2023-01-23 20:58

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='liketoanswer',
            managers=[
                ('manager', django.db.models.manager.Manager()),
            ],
        ),
    ]
