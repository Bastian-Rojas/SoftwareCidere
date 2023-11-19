import re
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

def index(request):
    return render(request, 'index.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            validate_email(username)
        except ValidationError:
            return render(request, 'login.html', {'error': 'Por favor, ingrese un correo electrónico válido'})
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página principal después del inicio de sesión
        else:
            # Mensaje de error si el inicio de sesión falla
            return render(request, 'login.html', {'error': 'Usuario o contraseña inválidos'})
    else:
        return render(request, 'login.html')

def is_valid_rut(rut):
    # Función para validar el formato del RUT utilizando una expresión regular
    rut_pattern = re.compile(r'^\d{1,8}-\d{1,2}$')
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

        # Validar que las contraseñas coincidan
        if password != repassword:
            return render(request, 'register.html', {'error': 'Las contraseñas no coinciden'})
        
         # Validar el formato del correo electrónico
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'register.html', {'error': 'Por favor, ingrese un correo electrónico válido'})
        
        if not is_valid_rut(rutempresa):
            return render(request, 'register.html', {'error': 'Por favor, ingrese un RUT válido'})
        
        if not numcontact.isdigit() or len(numcontact) > 9:
            return render(request, 'register.html', {'error': 'Por favor, ingrese un número de contacto válido'})

        # Crear un nuevo usuario
        user = User.objects.create_user(username=username, email=email, password=password)

        # Guardar información adicional en el perfil del usuario
        user.profile.rutempresa = rutempresa
        user.profile.tipotrabajo = tipotrabajo
        user.profile.tipoempresa = tipoempresa
        user.profile.servofre = servofre
        user.profile.numcontact = numcontact
        user.profile.descripcion = descripcion

        # Guardar el usuario y redirigir a la página de inicio de sesión
        user.save()
        login(request, user)
        return redirect('login')
    else:
        return render(request, 'register.html')