from django.db import models

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    rut_empresa = models.CharField(max_length=20, unique=True)  
    tipo_trabajo = models.CharField(max_length=50)
    tipo_empresa = models.CharField(max_length=50)
    servicio_ofrecido = models.CharField(max_length=200)  
    numero_contacto = models.CharField(max_length=20, unique=True) 
    correo_contacto = models.EmailField()
    descripcion = models.TextField()  
    calificacion = models.DecimalField(max_digits=3, decimal_places=2) 

    def __str__(self):
        return self.nombre