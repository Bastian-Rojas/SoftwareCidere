from django.shortcuts import render
from .models import Usuario, Region, Provincia, Comuna, Tipo_Empresa, Rubro, Tamano_Empresa

def index(request):
    usuarios = Usuario.objects.all()
    regiones = Region.objects.all()
    provincias = Provincia.objects.all()
    comunas = Comuna.objects.all()
    tipos_empresa = Tipo_Empresa.objects.all()
    rubros = Rubro.objects.all()
    tamanos_empresa = Tamano_Empresa.objects.all()

    context = {
        'usuarios': usuarios,
        'regiones': regiones,
        'provincias': provincias,
        'comunas': comunas,
        'tipos_empresa': tipos_empresa,
        'rubros': rubros,
        'tamanos_empresa': tamanos_empresa,
    }
    return render(request, '.html', context)