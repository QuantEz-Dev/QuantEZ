# Generated by Django 4.2.5 on 2023-11-02 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backtesting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signup',
            name='strategy',
            field=models.CharField(choices=[('GC', 'Golden Cross'), ('ATR', 'ATR'), ('rsi', 'RSI'), ('bollingerbands', 'Bollingerbands'), ('smacross', 'SmaCross')], default='GC', max_length=100),
        ),
    ]
