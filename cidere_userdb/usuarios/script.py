from django.shortcuts import render
from .models import Servicio, Usuario

def servicios(request):
    # Obtener parámetros de la URL
    search_query = request.GET.get('search', '')

    # Filtrar servicios según la búsqueda
    resultados = Usuario.objects.filter(nombre__icontains=search_query)

    # Renderizar la página de resultados de búsqueda
    return render(request, 'resultados_busqueda.html', {'servicios': resultados, 'query': search_query})
