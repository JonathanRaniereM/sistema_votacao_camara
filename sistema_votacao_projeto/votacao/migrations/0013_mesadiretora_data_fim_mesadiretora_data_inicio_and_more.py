# Generated by Django 4.2.4 on 2023-09-04 12:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votacao', '0012_mesadiretora_presenca_presenca_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mesadiretora',
            name='data_fim',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mesadiretora',
            name='data_inicio',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vereador',
            name='mesa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='votacao.mesadiretora'),
        ),
    ]
