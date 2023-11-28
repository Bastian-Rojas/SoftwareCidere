from django.shortcuts import render
from .models import Servicio

def servicios(request):
    servicios_list = Servicio.objects.all()

    # Obtener parámetros de la URL
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', '')

    # Aplicar filtros y ordenación
    if search_query:
        servicios_list = servicios_list.filter(nombre__icontains=search_query)

    if order_by:
        servicios_list = servicios_list.order_by(order_by)

    return render(request, 'servicios.html', {'servicios': servicios_list})
