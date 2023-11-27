from django import forms
from .models import Usuario

class UsuarioRegistrationForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    repassword = forms.CharField(widget=forms.PasswordInput, label='Repetir contraseña')

    class Meta:
        model = Usuario
        fields = ['nombre', 'contraseña', 'rut_empresa', 'tipo_trabajo', 'tipo_empresa', 'servicio_ofrecido', 'numero_contacto', 'correo_contacto', 'descripcion']