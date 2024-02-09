# Generated by Django 4.2.6 on 2023-10-09 13:34

from django.db import migrations, models
import votacao.models


class Migration(migrations.Migration):

    dependencies = [
        ('votacao', '0025_partidopolitico_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partidopolitico',
            name='logo',
            field=models.FileField(null=True, upload_to='logo_partido/', validators=[votacao.models.validate_file_extension]),
        ),
    ]
