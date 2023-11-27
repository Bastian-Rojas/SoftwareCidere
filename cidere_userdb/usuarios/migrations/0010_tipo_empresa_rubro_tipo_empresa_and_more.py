# Generated by Django 4.2.6 on 2023-11-27 17:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_region_rubro_remove_usuario_calificacion_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tipo_Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='rubro',
            name='tipo_empresa',
            field=models.ForeignKey(default=123, on_delete=django.db.models.deletion.CASCADE, to='usuarios.tipo_empresa'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='tipo_empresa',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='usuarios.tipo_empresa'),
        ),
    ]
