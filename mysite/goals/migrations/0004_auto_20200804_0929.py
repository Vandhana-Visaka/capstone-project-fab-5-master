# Generated by Django 3.0.7 on 2020-08-04 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_goal_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goal',
            name='month',
            field=models.IntegerField(default=8),
        ),
    ]
