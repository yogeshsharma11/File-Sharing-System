# Generated by Django 5.1.5 on 2025-02-09 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_folder_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
