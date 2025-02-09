from django.db import migrations, models
import app.models

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_folder_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='uid',
            field=models.CharField(default=app.models.generate_short_uid, editable=False, max_length=8, primary_key=True),
        ),
    ] 