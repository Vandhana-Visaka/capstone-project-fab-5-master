# Generated by Django 3.0.7 on 2020-07-08 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercollections', '0006_auto_20200708_0601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collection',
            name='books',
        ),
    ]
