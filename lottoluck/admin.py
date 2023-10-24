from django.contrib import admin
from .models import Sorteos
from .models import Clientes
from .models import Casagrande
from .models import Vendedor
from .models import NumeroSorteados
from .models import Numero
from .models import VtasSorteo
from .models import VtasDetalle
from .models import Secuencia

from django.utils.html import format_html


class ClientesAdmin(admin.ModelAdmin):
    list_display = ("display_imagen", "cedula", "nombre",
                    "apellido", "gender", "email", "telefono", )
    search_fields = ("cedula", "nombre", "apellido", "email")
    list_filter = ("cedula", "nombre", "apellido", "email")
    list_editable = ["gender"]
    list_per_page = 15
    # readonly_fields = ("display_imagen_admin",)

    # def display_imagen(self, obj):
    #    return format_html('<div style="width: 50px; height: 50px; border-radius: 50%; overflow: hidden;"><img src="{}" style="width: 100%; height: 100%; object-fit: cover;" /></div>', obj.imagen.url)

    # def display_imagen_admin(self, obj):
    #    return format_html('<div style="width: 100px; height: 100px; border-radius: 50%; overflow: hidden;"><img src="{}" style="width: 100%; height: 100%; object-fit: cover;" /></div>', obj.imagen.url)

    # display_imagen.short_description = "Foto"
    # display_imagen_admin.short_description = "Foto Actual"

    # def display_imagen1(self, obj):
    #    if obj.imagen:
    #        return format_html('<div style="width: 50px; height: 50px; border-radius: 50%; overflow: hidden;"><img src="{}" style="width: 100%; height: 100%; object-fit: cover;" /></div>', obj.imagen.url)

    #    else:
    #        return "N/A"

    # display_imagen.short_description = "Imagen"


admin.site.register(Sorteos)

admin.site.register(Clientes)
admin.site.register(Casagrande)
admin.site.register(Vendedor)
admin.site.register(Secuencia)


class NumeroSorteadosAdmin(admin.ModelAdmin):
    list_display = ("fecha", "referencia", "I_premio", "letras",
                    "serie", "folio", "II_premio", "III_premio")
    search_fields = ("fecha", "referencia", "I_premio", "letras", "serie", "folio",
                     "II_premio", "III_premio")  # Cambia "tipo" al campo correcto en Sorteos
    list_filter = ("fecha", "referencia", "I_premio", "letras", "serie", "folio",
                   "II_premio", "III_premio")  # Cambia "tipo" al campo correcto en Sorteos

    def fecha_sorteo(self, obj):
        return obj.fecha.strftime('%Y-%m-%d')

    fecha_sorteo.short_description = "Fecha del Sorteo"


admin.site.register(NumeroSorteados, NumeroSorteadosAdmin)


class NumeroAdmin(admin.ModelAdmin):
    list_display = ("numero", "limite", "activo", "display_imagen1",)
    search_fields = ("numero", "limite", "activo", "imagen")
    list_filter = ("numero", "limite", "activo", "imagen")
    list_per_page = 15

    def display_imagen(self, obj):
        return format_html('<div style="width: 50px; height: 50px; border-radius: 50%; overflow: hidden;"><img src="{}" style="width: 100%; height: 100%; object-fit: cover;" /></div>', obj.imagen.url)

    def display_imagen_admin(self, obj):
        return format_html('<div style="width: 100px; height: 100px; border-radius: 50%; overflow: hidden;"><img src="{}" style="width: 100%; height: 100%; object-fit: cover;" /></div>', obj.imagen.url)

    display_imagen.short_description = "Foto"
    display_imagen_admin.short_description = "Foto Actual"

    def display_imagen1(self, obj):
        if obj.imagen:
            return format_html('<div style="width: 50px; height: 50px; border-radius: 50%; overflow: hidden;"><img src="{}" style="width: 100%; height: 100%; object-fit: cover;" /></div>', obj.imagen.url)

        else:
            return "N/A"


admin.site.register(Numero, NumeroAdmin)
admin.site.register(VtasSorteo)
admin.site.register(VtasDetalle)

# Register your models here.
