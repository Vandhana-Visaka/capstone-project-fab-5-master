# Generated by Django 3.0.7 on 2020-06-28 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='collecions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collectionName', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('createdDate', models.DateTimeField()),
                ('UID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('books', models.ManyToManyField(to='books.Books')),
            ],
        ),
    ]
