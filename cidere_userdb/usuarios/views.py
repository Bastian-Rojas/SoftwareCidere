import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, hashers
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Usuario, Provincia, Comuna, Region, Rubro

def cargar_regiones(request):
    regiones = Region.objects.all().order_by('nombre')
    return JsonResponse(list(regiones.values('id', 'nombre')), safe=False)

def cargar_provincias(request):
    region_id = request.GET.get('region_id')
    provincias = Provincia.objects.filter(region_id=region_id).order_by('nombre')
    return JsonResponse(list(provincias.values('id', 'nombre')), safe=False)

def cargar_comunas(request):
    provincia_id = request.GET.get('provincia_id')
    comunas = Comuna.objects.filter(provincia_id=provincia_id).order_by('nombre')
    return JsonResponse(list(comunas.values('id', 'nombre')), safe=False)

def cargar_rubros(request):
    rubros = Rubro.objects.all().order_by('nombre')
    return JsonResponse(list(rubros.values('id', 'nombre')), safe=False)
    

def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'login.html', {'error': 'Email y contraseña son obligatorios'})

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'login.html', {'error': 'Por favor, ingrese un correo electrónico válido'})

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
        username = request.POST['username']
        rutempresa = request.POST['rutempresa']
        tipotrabajo = request.POST['tipotrabajo']
        tipoempresa = request.POST['tipoempresa']
        servofre = request.POST['servofre']
        numcontact = request.POST['numcontact']
        email = request.POST['email']
        descripcion = request.POST['descripcion']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password != repassword:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'register.html', {'error': 'Por favor, ingrese un correo electrónico válido'})

        if not is_valid_rut(rutempresa):
            return render(request, 'register.html', {'error': 'Por favor, ingrese un RUT válido'})

        if not numcontact.isdigit() or len(numcontact) > 9:
            return render(request, 'register.html', {'error': 'Por favor, ingrese un número de contacto válido'})

        nuevo_usuario = Usuario(
            nombre=username,
            rut_empresa=rutempresa,
            tipo_trabajo=tipotrabajo,
            tipo_empresa=tipoempresa,
            servicio_ofrecido=servofre,
            numero_contacto=numcontact,
            correo_contacto=email,
            descripcion=descripcion,
            # calificacion - Asegúrate de manejar esto según tus requisitos
        )
        nuevo_usuario.set_password(password)  # Establece la contraseña de forma segura
        nuevo_usuario.save()
        return redirect('login')
    else:
        return render(request, 'register.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('index')