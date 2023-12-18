import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, hashers
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Usuario, Provincia, Comuna, Region, Rubro, Tipo_Empresa, Tamano_Empresa, Servicio, Encuesta
from django.db.models import Q


def cargar_regiones(request):
    regiones = Region.objects.all().order_by('id')
    return JsonResponse(list(regiones.values('id', 'nombre')), safe=False)

def cargar_tipo_empresa(request):
    regiones = Tipo_Empresa.objects.all().order_by('id')
    return JsonResponse(list(regiones.values('id', 'nombre')), safe=False)

def cargar_provincias(request):
    region_id = request.GET.get('region_id')  # Se espera que 'region_id' sea pasado como parámetro en la URL
    provincias = Provincia.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(provincias.values('id', 'nombre')), safe=False)

def cargar_comunas(request):
    provincia_id = request.GET.get('provincia_id')
    comunas = Comuna.objects.filter(provincia_id=provincia_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)

def cargar_rubros(request):
    tipo_empresa_id = request.GET.get('tipo_empresa_id')
    rubros = Rubro.objects.filter(tipo_empresa_id=tipo_empresa_id).order_by('nombre')
    return JsonResponse(list(rubros.values('id', 'nombre')), safe=False)

def cargar_tamanos_empresa(request):
    tamanos = Tamano_Empresa.objects.all().order_by('nombre')
    return JsonResponse(list(tamanos.values('id', 'nombre')), safe=False)


def index(request):
    return render(request, 'index.html')

def validate_rut(rut):
    pattern = re.compile(r'^\d{2}\.\d{3}\.\d{3}-[\dkK]$')
    if not pattern.match(rut):
        raise ValidationError('Formato de RUT inválido. Debe ser como 77.627.982-K.')

def user_login(request):
    if request.method == 'POST':
        rut_empresa = request.POST.get('rut_empresa')
        password = request.POST.get('password')

        if not rut_empresa or not password:
            return render(request, 'login.html', {'error': 'RUT y contraseña son obligatorios'})

        try:
            validate_rut(rut_empresa)
        except ValidationError:
            return render(request, 'login.html', {'error': 'Por favor, ingrese un RUT válido'})

        # Intentar autenticar al usuario
        usuario = authenticate(request, username=rut_empresa, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'RUT o contraseña incorrectos'})

    else:
        return render(request, 'login.html')

        
def is_valid_rut(rut):
    rut_pattern = re.compile(r'^\d{2}\.\d{3}\.\d{3}-[\dkK]$')
    return bool(rut_pattern.match(rut))

def user_register(request):
    if request.method == 'POST':
        rut_empresa = request.POST['rut_empresa']
        correo_contacto = request.POST['correo_contacto']
        nombre = request.POST['nombre']
        razon_social = request.POST['razon_social']
        region = request.POST['region']
        provincia = request.POST['provincia']
        comuna = request.POST['comuna']
        direccion = request.POST['direccion']
        tipo_empresa = request.POST['tipo_empresa']
        rubros = request.POST['rubros']
        tamano_empresa = request.POST['tamano_empresa']
        descripcion = request.POST['descripcion']
        sitio_web = request.POST['sitio_web']
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')

        region = Region.objects.get(id=region)
        provincia = Provincia.objects.get(id=provincia)
        comuna = Comuna.objects.get(id=comuna)
        tipo_empresa = Tipo_Empresa.objects.get(id=tipo_empresa)
        tamano_empresa = Tamano_Empresa.objects.get(id=tamano_empresa)

        if password != repassword:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})

        try:
            validate_email(correo_contacto)
        except ValidationError:
            return render(request, 'register.html', {'error': 'Por favor, ingrese un correo electrónico válido'})

        if not is_valid_rut(rut_empresa):
            return render(request, 'register.html', {'error': 'Por favor, ingrese un RUT válido'})

        nuevo_usuario = Usuario(
            rut_empresa=rut_empresa,
            correo_contacto=correo_contacto,
            nombre=nombre,
            razon_social=razon_social,
            region=region,
            provincia=provincia,
            comuna=comuna,
            direccion=direccion,
            tipo_empresa=tipo_empresa,
            tamano_empresa=tamano_empresa,
            descripcion=descripcion,
            sitio_web=sitio_web
        )
        nuevo_usuario.set_password(password)  # Establece la contraseña de forma segura
        nuevo_usuario.save()

        # Obtiene los IDs de rubros seleccionados y los asocia al nuevo usuario
        rubros_seleccionados = request.POST.getlist('rubros')
        for rubro_id in rubros_seleccionados:
            rubro = Rubro.objects.get(id=rubro_id)
            nuevo_usuario.rubros.add(rubro)

        return redirect('index')
    else:
        return render(request, 'register.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('index')

from django.shortcuts import render
from django.http import JsonResponse
from .models import Usuario, Tipo_Empresa, Rubro
from django.db.models import Q

def resultado_busqueda(request):
    if request.method == 'POST':
        query = request.POST.get('query', '').strip()
        orden = request.POST.get('orden', 'A-Z')
        tipo_empresa_id = request.POST.getlist('tipo_empresa')
        rubro_id = request.POST.getlist('rubro')

        queryset = Usuario.objects.all()

        if query:
            palabras_busqueda = query.split(" ")
            for palabra in palabras_busqueda:
                queryset = queryset.filter(
                    Q(nombre__icontains=palabra) |
                    Q(tipo_empresa__nombre__icontains=palabra) |
                    Q(rubros__nombre__icontains=palabra)
                )

        if tipo_empresa_id:
            queryset = queryset.filter(tipo_empresa__id__in=tipo_empresa_id)

        if rubro_id:
            queryset = queryset.filter(rubros__id__in=rubro_id)

        if orden == 'Z-A':
            queryset = queryset.order_by('-nombre')
        else:
            queryset = queryset.order_by('nombre')

        # Verificar si la solicitud es AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            usuarios = queryset.distinct().values('nombre', 'tipo_empresa__nombre', 'rubros__nombre')
            return JsonResponse({'usuarios': list(usuarios)})
        else:
            usuarios = queryset.distinct()
            tipos_empresa = Tipo_Empresa.objects.all()
            rubros = Rubro.objects.all()
            return render(request, 'resultados_busqueda.html', {'usuarios': usuarios, 'query': query, 'tipos_empresa': tipos_empresa, 'rubros': rubros})
    else:
        # Manejar casos que no son POST (puede ser GET u otros)
        # Aquí puedes decidir qué hacer, como mostrar un formulario de búsqueda vacío o redirigir
        tipos_empresa = Tipo_Empresa.objects.all()
        rubros = Rubro.objects.all()
        return render(request, 'resultados_busqueda.html', {'tipos_empresa': tipos_empresa, 'rubros': rubros})

def resultado_sugerencias(request):
    if request.method == 'GET':
        query = request.GET.get('query', '')
        if query:
            palabras_busqueda = query.split(" ")
            queryset = Usuario.objects.all()

            for palabra in palabras_busqueda:
                queryset = queryset.filter(
                    Q(nombre__icontains=palabra) |
                    Q(tipo_empresa__nombre__icontains=palabra) |
                    Q(rubros__nombre__icontains=palabra)
                )
            usuarios = queryset.distinct().values('nombre')  # Cambia 'nombre' por los campos que necesites
            return JsonResponse({'usuarios': list(usuarios), 'query': query})

    return JsonResponse({'error': 'Método no permitido'}, status=405)

def cargar_encuestas(request):
    if request.method == 'POST':
        print('test2')
        cont_proveedores = request.POST.get('contProve', 0)
        cont_servicios = request.POST.get('contServ', 0)
        calificacion_sitio = request.POST.get('rating', 0)
        terminos_y_condiciones = request.POST.get('terminos') == 'on'

        # Obtener el usuario actualmente autenticado
        usuario_actual = request.user

        # Crear una nueva Encuesta asociada al usuario actual
        encuesta = Encuesta.objects.create(
            usuario=usuario_actual,
            cont_proveedores=cont_proveedores,
            cont_servicios=cont_servicios,
            calificacion_sitio=calificacion_sitio,
            terminos_y_condiciones=terminos_y_condiciones
        )
        encuesta.save()
        print(encuesta)

        # Redireccionar a alguna página después de guardar los datos
        return redirect('index')  # Cambia '/gracias/' por la URL que desees
    print('test')
    return render(request, 'encuestas.html')