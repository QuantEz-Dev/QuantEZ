# Generated by Django 4.2.5 on 2023-11-16 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backtesting', '0009_signup_commission'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signup',
            name='commission',
        ),
    ]