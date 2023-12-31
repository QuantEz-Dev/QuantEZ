# Generated by Django 4.2.5 on 2023-11-02 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('assetmanagement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='asset',
            name='create_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
