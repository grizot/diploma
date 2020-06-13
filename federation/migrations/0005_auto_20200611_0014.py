# Generated by Django 2.2.2 on 2020-06-10 21:14

from django.db import migrations, models
import federation.models
import federation.validators


class Migration(migrations.Migration):

    dependencies = [
        ('federation', '0004_auto_20200610_2243'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='federationstaff',
            name='imageOld',
        ),
        migrations.AlterField(
            model_name='federationstaff',
            name='image',
            field=models.ImageField(default='', upload_to=federation.models.FederationStaff.user_directory_path, validators=[federation.validators.validate_image], verbose_name='Фото'),
        ),
    ]