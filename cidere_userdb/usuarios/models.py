from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, correo_contacto, password=None, **extra_fields):
        if not correo_contacto:
            raise ValueError('Los usuarios deben tener una dirección de correo electrónico')
        user = self.model(correo_contacto=self.normalize_email(correo_contacto), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_contacto, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')

        return self.create_user(correo_contacto, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    nombre = models.CharField(max_length=100)
    rut_empresa = models.CharField(max_length=20, unique=True)  
    tipo_trabajo = models.CharField(max_length=50)
    tipo_empresa = models.CharField(max_length=50)
    servicio_ofrecido = models.CharField(max_length=200)  
    numero_contacto = models.CharField(max_length=20, unique=True) 
    correo_contacto = models.EmailField(unique=True)
    descripcion = models.TextField()  
    calificacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    # Campos requeridos por Django para el modelo de usuario
    is_staff = models.BooleanField(default=False)  # Indica si el usuario puede acceder al sitio de administración
    is_active = models.BooleanField(default=True)  # Indica si el usuario está activo

    objects = CustomUserManager()

    USERNAME_FIELD = 'correo_contacto'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
