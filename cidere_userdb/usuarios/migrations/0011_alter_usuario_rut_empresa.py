# Generated by Django 4.2.6 on 2023-11-27 22:11

from django.db import migrations, models
import usuarios.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0010_tipo_empresa_rubro_tipo_empresa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rut_empresa',
            field=models.CharField(max_length=20, unique=True, validators=[usuarios.models.validate_rut]),
        ),
    ]
