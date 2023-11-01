from django.urls import path, include
from lottoluck import views
from django.conf import settings
from django.conf.urls.static import static
from .views import ClientesListView, agregar_numero, eliminar_numero, limpiar_numero, restar_numero, ver_carrito
from .views import CustomLogoutView

from django.views.decorators.http import require_http_methods
urlpatterns = [
    #  path(''                                ,views.lista_clientes , name='lista_clientes'),
    path('lista_clientes/', views.lista_clientes, name='lista_clientes'),
    path('index/', views.contadores, name='contadores'),
    path('init_numeros/', views.init_numeros, name='init_numeros'),
    path('editar_cliente/<int:cliente_id>/',
         views.editar_cliente, name='editar_cliente'),
    path('add_cliente/', views.add_cliente, name='add_cliente'),
    path('borrar_cliente/<int:cliente_id>/',
         views.borrar_cliente, name='borrar_cliente'),
    path('generate_fake_clients/', views.generate_fake_clients,
         name='generate_fake_clients'),

    path('ventas/', views.venta_Numeros, name='venta_Numeros'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('agregar/<int:numero_id>/<int:desdecatalogo>',
         agregar_numero, name='add'),
    path('eliminar/<int:numero_id>/', eliminar_numero, name='del'),
    path('restar/<int:numero_id>/', restar_numero, name='sub'),
    path('limpiar/', limpiar_numero, name='CLS'),
    path('micompra/', ver_carrito,  name='vercarrito'),
    path('consultar_cliente/', views.consultar_cliente, name='consultar_cliente'),
    path('pagar/', views.pagar, name='pagar'),
    path('generar_ticket_pdf/',
         views.generar_ticket_pdf, name='generar_ticket_pdf'),

    path('descargar_pdf/<int:vtas_sorteo_id>/',
         views.descargar_pdf, name='descargar_pdf'),
    path('ventaSorteo/', views.ventaSorteo, name='ventaSorteo'),
    path('consultasorteo/', views.consultasorteo, name='consultasorteo'),
    path('compradoresdelNumero/<int:numero_id>', views.compradoresdelNumero,
         name='compradoresdelNumero'),
    path('detalle_cliente/<str:numero>/<int:id_sorteo>/<str:fecha_sorteo>/',
         views.detalle_cliente_y_ticket, name='detalle_cliente'),

    path('listapdf/<str:pdf_content>/', views.listapdf, name='listapdf'),

    path('lista_numero_sorteados/', views.lista_numero_sorteados,
         name='lista_numero_sorteados'),
    path('editar_numero_sorteados/<int:numero_sorteados_id>/',
         views.editar_numero_sorteados, name='editar_numero_sorteados'),
    path('agregar_numero_sorteados/', views.agregar_numero_sorteados,
         name='agregar_numero_sorteados'),
    # path('agregar_numero_sorteados/', views.agregar_numero_sorteados,
    #    name='agregar_numero_sorteados'),
    # path("unicorn/", include("django_unicorn.urls")),
    path('get-items/', views.get_items, name='get_items'),
    path('buscar_venta/', views.buscar_venta, name='buscar_venta'),

    path('ticket/<str:transaction_id>/',
         views.detalle_venta_ticket, name='ticket'),
    path('comprasctes/<int:numero_cliente>/',
         views.historial_compra_cliente, name='comprasctes'),
    path('ganadores/<str:id_sorteo>/<str:fecha>/<int:premio1>/<int:premio2>/<int:premio3>/',
         views.ganadores, name='ganadores'),






]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
