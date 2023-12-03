from django.contrib import admin
from .models import Usuario,Region, Provincia, Comuna, Rubro, Tipo_Empresa, Tamano_Empresa, Servicio, Encuesta

admin.site.register(Usuario)
admin.site.register(Region)
admin.site.register(Provincia)
admin.site.register(Comuna)
admin.site.register(Rubro)
admin.site.register(Tipo_Empresa)
admin.site.register(Tamano_Empresa)
admin.site.register(Servicio)
admin.site.register(Encuesta)