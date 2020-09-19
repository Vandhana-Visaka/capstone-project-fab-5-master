# Generated by Django 3.0.7 on 2020-07-08 00:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0002_auto_20200629_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('review', models.TextField()),
                ('BID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='books.Books')),
                ('UID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reviews',
                'verbose_name_plural': 'Reviews',
            },
        ),
    ]
