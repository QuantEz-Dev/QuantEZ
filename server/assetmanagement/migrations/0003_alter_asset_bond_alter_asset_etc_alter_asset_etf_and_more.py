# Generated by Django 4.2.5 on 2023-11-02 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assetmanagement', '0002_alter_asset_author_alter_asset_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='bond',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='etc',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='etf',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='fund',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
