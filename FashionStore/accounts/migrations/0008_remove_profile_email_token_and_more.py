# Generated by Django 4.2.1 on 2023-05-31 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_profile_password_profile_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email_token',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_email_vertified',
        ),
    ]
