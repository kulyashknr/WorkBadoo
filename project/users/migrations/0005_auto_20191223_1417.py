# Generated by Django 2.2.1 on 2019-12-23 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.upload
import utils.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_worker_industry'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=utils.upload.user_photo_path, validators=[utils.validators.validate_size, utils.validators.validate_extension]),
        ),
        migrations.AddField(
            model_name='worker',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=utils.upload.user_photo_path, validators=[utils.validators.validate_size, utils.validators.validate_extension]),
        ),
        migrations.AlterField(
            model_name='worker',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='worker_user', to=settings.AUTH_USER_MODEL),
        ),
    ]