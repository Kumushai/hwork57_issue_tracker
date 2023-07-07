# Generated by Django 4.2.3 on 2023-07-07 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_remove_todo_type_todo_types'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='types',
        ),
        migrations.AddField(
            model_name='todo',
            name='types',
            field=models.ManyToManyField(blank=True, related_name='types', to='webapp.type'),
        ),
    ]
