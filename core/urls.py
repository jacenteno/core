"""lottolab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from lottoluck import views
from daskboard import views as daskboard_views  # Importa las vistas de darkboard
from django.views.generic.base import RedirectView
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from lottoluck.views import custom_logout  # Importa tu vista personalizada de cierre de sesión


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    #path('', lambda request: redirect('/lottoluck/contadores/')),  # Redirección de la página de inicio a la nueva ruta
    path('', lambda request: redirect('/lottoluck/contadores/', permanent=True)),  # Redirección permanente a la nueva ruta
    path('lottoluck/', RedirectView.as_view(pattern_name='contadores', permanent=False)),
 
    path('admin/', admin.site.urls),
    path('lottoluck/', daskboard_views.daskboard_principal, name='lottoluck_home'),
    path('lottoluck/', include('lottoluck.urls')),
    path('init_numeros/', views.init_numeros, name='init_numeros'),
 #  para autenticar.
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', include('lottoluck.urls')),  # Incluye las URLs de tu aplicación
    path('report/', include(('report.urls', 'report'))),
    
   
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)