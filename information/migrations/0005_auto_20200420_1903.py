# Generated by Django 2.2.2 on 2020-04-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0004_auto_20200420_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playershistory',
            name='end',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Покинул команду'),
        ),
    ]