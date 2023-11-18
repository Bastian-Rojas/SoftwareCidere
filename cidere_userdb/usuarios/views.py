from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def index(request):
    return render(request, 'index.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página principal después del inicio de sesión
        else:
            # Mensaje de error si el inicio de sesión falla
            return render(request, 'login.html', {'error': 'Usuario o contraseña inválidos'})
    else:
        return render(request, 'login.html')