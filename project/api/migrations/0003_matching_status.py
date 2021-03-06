# Generated by Django 2.2.1 on 2019-11-30 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20191130_1915'),
    ]

    operations = [
        migrations.AddField(
            model_name='matching',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'MATCHED_BY_COMPANY'), (2, 'MATCHED_BY_USER'), (3, 'MATCHED_BY_BOTH'), (4, 'DECLINED_BY_USER'), (5, 'DECLINED_BY_COMPANY')], default=1),
            preserve_default=False,
        ),
    ]
