# Generated by Django 4.2.6 on 2023-11-28 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0011_alter_usuario_rut_empresa'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tamano_Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
    ]
