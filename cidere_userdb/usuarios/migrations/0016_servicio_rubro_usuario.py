# Generated by Django 4.2.7 on 2023-12-01 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0015_servicio_nombre_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicio',
            name='rubro_usuario',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]