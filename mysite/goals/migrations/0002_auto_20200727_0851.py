# Generated by Django 3.0.7 on 2020-07-27 08:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goals', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='month',
            field=models.IntegerField(default=7),
        ),
        migrations.AddField(
            model_name='goal',
            name='year',
            field=models.IntegerField(default=2020),
        ),
        migrations.AlterUniqueTogether(
            name='goal',
            unique_together={('UID', 'year', 'month')},
        ),
        migrations.RemoveField(
            model_name='goal',
            name='goalDate',
        ),
    ]
