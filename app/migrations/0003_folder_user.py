from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_rename_craeted_at_folder_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='user',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                null=True  # Allow null temporarily for existing records
            ),
        ),
    ] 