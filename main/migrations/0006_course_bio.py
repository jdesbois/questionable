# Generated by Django 2.1.5 on 2020-03-18 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_merge_20200318_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='bio',
            field=models.CharField(blank=True, default=None, max_length=1024, null=True),
        ),
    ]
