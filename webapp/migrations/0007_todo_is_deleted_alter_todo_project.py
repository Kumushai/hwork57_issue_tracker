# Generated by Django 4.2.3 on 2023-07-18 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_alter_project_options_rename_projects_todo_project_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='todo',
            name='project',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='webapp.project', verbose_name='Проект'),
        ),
    ]
