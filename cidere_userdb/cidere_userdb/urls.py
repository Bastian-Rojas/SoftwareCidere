"""
URL configuration for cidere_userdb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from usuarios import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('cargar-provincias/', views.cargar_provincias, name='cargar_provincias'),
    path('cargar-comunas/', views.cargar_comunas, name='cargar_comunas'),
    path('cargar-regiones/', views.cargar_regiones, name='cargar_regiones'),
    path('cargar-rubros/', views.cargar_rubros, name='cargar_rubros'),
    path('cargar-tipo_empresa/', views.cargar_tipo_empresa, name='cargar_tipo_empresa'),
    path('cargar-tamanos_empresa/', views.cargar_tamanos_empresa, name='cargar_tamanos_empresa'),
    path('resultados/', views.resultado_busqueda, name='resultados'),
    path('encuestas/', views.cargar_encuestas, name='cargar_encuestas'),
]
