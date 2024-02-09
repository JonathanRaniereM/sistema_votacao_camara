# Generated by Django 4.2.6 on 2023-10-24 12:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votacao', '0026_alter_partidopolitico_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='pauta',
            name='autor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pautas_autoradas', to='votacao.vereador'),
        ),
        migrations.AddField(
            model_name='pauta',
            name='documento',
            field=models.URLField(blank=True, null=True, validators=[django.core.validators.URLValidator()]),
        ),
    ]
