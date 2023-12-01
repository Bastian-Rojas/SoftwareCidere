from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.db import models
import re

def validate_rut(rut):
    pattern = re.compile(r'^\d{2}\.\d{3}\.\d{3}-[\dkK]$')
    if not pattern.match(rut):
        raise ValidationError('Formato de RUT inválido. Debe ser como 77.627.982-K.')
    
class Tipo_Empresa(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Provincia(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Rubro(models.Model):
    tipo_empresa = models.ForeignKey(Tipo_Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Tamano_Empresa(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
class Usuario(AbstractBaseUser, PermissionsMixin):
    rut_empresa = models.CharField(max_length=20, unique=True, validators=[validate_rut])  
    correo_contacto = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True)
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True)
    direccion = models.CharField(max_length=200)
    tipo_empresa = models.ForeignKey(Tipo_Empresa, on_delete=models.SET_NULL, null=True)
    rubros = models.ManyToManyField(Rubro)
    tamano_empresa = models.ForeignKey(Tamano_Empresa, on_delete=models.SET_NULL, null=True)
    descripcion = models.TextField()
    sitio_web = models.URLField(blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='usuarios')
    user_permissions = models.ManyToManyField(Permission, related_name='usuarios_permissions')