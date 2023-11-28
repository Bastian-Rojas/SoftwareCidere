from django import forms
from .models import Usuario, Region, Provincia, Comuna, Tipo_Empresa, Rubro

class UsuarioRegistrationForm(forms.ModelForm):
    contraseña = forms.CharField(widget=forms.PasswordInput)
    repassword = forms.CharField(widget=forms.PasswordInput, label='Repetir contraseña')
    region = forms.ModelChoiceField(queryset=Region.objects.all(), required=False)
    provincia = forms.ModelChoiceField(queryset=Provincia.objects.all(), required=False)
    comuna = forms.ModelChoiceField(queryset=Comuna.objects.all(), required=False)
    tipo_empresa = forms.ModelChoiceField(queryset=Tipo_Empresa.objects.all(), required=False)
    rubros = forms.ModelMultipleChoiceField(queryset=Rubro.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'rut_empresa', 'correo_contacto', 'razon_social', 'region', 'provincia', 'comuna', 'direccion', 'tipo_empresa', 'rubros', 'tamano_empresa', 'descripcion', 'sitio_web', 'contraseña']

    def clean(self):
        cleaned_data = super().clean()
        contraseña = cleaned_data.get("contraseña")
        repassword = cleaned_data.get("repassword")

        if contraseña != repassword:
            raise forms.ValidationError("Las contraseñas no coinciden.")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["contraseña"])
        if commit:
            user.save()
        return user