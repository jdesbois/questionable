# Generated by Django 2.1.5 on 2020-03-08 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_course_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='user',
        ),
    ]
