# Generated by Django 2.2.2 on 2020-04-23 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_auto_20200423_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='away',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='awaygames', to='tournaments.Competitor', verbose_name='Гостевая команда'),
        ),
        migrations.AlterField(
            model_name='game',
            name='home',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='homegames', to='tournaments.Competitor', verbose_name='Домашняя команда'),
        ),
        migrations.AlterField(
            model_name='game',
            name='round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tournaments.Round', verbose_name='Тур'),
        ),
    ]
