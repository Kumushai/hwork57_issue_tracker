# Generated by Django 4.2.3 on 2023-07-25 07:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('webapp', '0008_project_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
