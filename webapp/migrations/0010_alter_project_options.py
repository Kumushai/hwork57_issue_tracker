# Generated by Django 4.2.3 on 2023-07-25 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0009_alter_project_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('add_project_user', 'Добавить юзера в проект'), ('change_project_user', 'Обновить юзера в проекте'), ('delete_project_user', 'Удалить юзера из проекта')], 'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
    ]