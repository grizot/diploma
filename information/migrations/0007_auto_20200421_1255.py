# Generated by Django 2.2.2 on 2020-04-21 09:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('information', '0006_auto_20200421_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='playershistory',
            name='player',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='information.Player', verbose_name='Игрок'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='playershistory',
            name='team',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='information.Team', verbose_name='Команда'),
            preserve_default=False,
        ),
    ]