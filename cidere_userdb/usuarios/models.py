from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
import re

def validate_rut(rut):
    pattern = re.compile(r'^\d{2}\.\d{3}\.\d{3}-[\dkK]$')
    if not pattern.match(rut):
        raise ValidationError('Formato de RUT inválido. Debe ser como 77.627.982-K.')
    
# Modelos para regiones, provincias y comunas}

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

# Modelo para rubros de la empresa
class Rubro(models.Model):
    tipo_empresa = models.ForeignKey(Tipo_Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Tamano_Empresa(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class CustomUserManager(BaseUserManager):
    def create_user(self, rut_empresa, password=None, **extra_fields):
        if not rut_empresa:
            raise ValueError('Los usuarios deben tener RUT de empresa')
        user = self.model(rut_empresa=rut_empresa, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, rut_empresa, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(rut_empresa, password, **extra_fields)

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

    # Campos requeridos por Django para el modelo de usuario
    is_staff = models.BooleanField(default=False)  # Indica si el usuario puede acceder al sitio de administración
    is_active = models.BooleanField(default=True)  # Indica si el usuario está activo

    objects = CustomUserManager()

    USERNAME_FIELD = 'rut_empresa'
    REQUIRED_FIELDS = ['nombre','correo_contacto']

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
