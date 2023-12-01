# Generated by Django 3.2.3 on 2023-12-01 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0014_servicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalificacionSitio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calificacion', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('fecha_registro', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactoProveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proveedores_contactados', models.PositiveIntegerField(default=0)),
                ('fecha_registro', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='ContactoServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servicios_brindados', models.PositiveIntegerField(default=0)),
                ('fecha_registro', models.DateField()),
            ],
        ),
    ]
