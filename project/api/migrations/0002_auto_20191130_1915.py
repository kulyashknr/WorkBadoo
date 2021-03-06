# Generated by Django 2.1.1 on 2019-11-30 19:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('api', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacancy_creator', to='users.Company'),
        ),
        migrations.AddField(
            model_name='matchingforworker',
            name='vacancies',
            field=models.ManyToManyField(to='api.Vacancy'),
        ),
        migrations.AddField(
            model_name='matchingforworker',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='matchforworker_worker', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='matchingforcompany',
            name='vacancy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='matchforcompany_vacancy', to='api.Vacancy'),
        ),
        migrations.AddField(
            model_name='matchingforcompany',
            name='workers',
            field=models.ManyToManyField(to='users.Worker'),
        ),
        migrations.AddField(
            model_name='matching',
            name='vacancy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='vacancy', to='api.Vacancy'),
        ),
        migrations.AddField(
            model_name='matching',
            name='worker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='worker', to=settings.AUTH_USER_MODEL),
        ),
    ]
