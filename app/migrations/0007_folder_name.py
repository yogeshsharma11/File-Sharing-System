from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_merge_files_and_folder'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ] 