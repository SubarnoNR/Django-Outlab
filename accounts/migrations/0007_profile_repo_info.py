# Generated by Django 3.2.7 on 2021-09-17 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='repo_info',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
