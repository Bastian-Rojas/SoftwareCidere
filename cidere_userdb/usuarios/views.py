import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, hashers
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Usuario, Provincia, Comuna, Region, Rubro, Tipo_Empresa, Tamano_Empresa

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
            return render(request, 'login.html', {'error': 'Por favor, ingrese un correo electrónico válido'})

        # Intentar autenticar al usuario
        usuario = authenticate(request, username=rut_empresa, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'RUT o contraseña incorrectos'})

    else:
        return render(request, 'login.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login.html', {'error': 'Email y contraseña son obligatorios'})

        

        usuario = authenticate(request, username=email, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Email o contraseña incorrecta'})

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

        return redirect('login')
    else:
        return render(request, 'register.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('index')