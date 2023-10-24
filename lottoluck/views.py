
from django.views.decorators.http import require_POST

from reportlab.lib.pagesizes import landscape
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.templatetags.static import static
from django.http import FileResponse

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from decimal import Decimal

from datetime import datetime
from django.contrib.humanize.templatetags.humanize import naturalday


from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from .models import Clientes, Vendedor, Sorteos, Casagrande, NumeroSorteados, VtasSorteo, VtasDetalle
from django.shortcuts import render, get_object_or_404, redirect

from .models import Clientes, Sorteos
from .forms import ClienteEditForm  # Importa el formulario de edición

from .forms import SorteosForm, ClienteForm
from .forms import ConsultaClienteForm, sorteo_vendedor_form
from .forms import VendedorForm, ClienteSeleccionForm, fechaValidaSorteoForm, fechaSorteoForm, NumeroSorteadosForm
from .models import Numero
from .models import Secuencia

from lottoluck.Carrito import Carrito  # Carrito de compra
import datetime

from django.views.generic import ListView
from django.db.models import Q  # Asegúrate de importar Q


from django.core.paginator import Paginator

from django.http import request
from django.contrib.auth.decorators import login_required

from django.core.management import call_command
from django.contrib.auth.views import LogoutView
from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse

# Para imprimir el PDF:
from django.http import FileResponse
from django.shortcuts import render
from django.contrib import messages


from reportlab.pdfgen import canvas
# Importa el tamaño de papel 'letter'
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from reportlab.lib.units import inch
from reportlab.graphics.barcode import code128


from io import BytesIO
from barcode import generate
from barcode.writer import ImageWriter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet


import barcode

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import landscape
from reportlab.lib.utils import ImageReader

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


from barcode import generate
from barcode.writer import ImageWriter
from barcode import generate
from barcode.writer import ImageWriter


from django.template.defaultfilters import capfirst
from django.utils.text import capfirst
# Importa la función del context processor
from lottoluck.context_processor import total_compra, total_qty, total_linea, factura_secuencia
from dateutil import parser as date_parser
import arrow
from django.core.files import File


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from weasyprint import HTML
from django.template import RequestContext
from django.template.loader import render_to_string


from twilio.rest import Client
from django.conf import settings

from django.db.models import Sum, F


def fecha_en_palabras(fecha):
    return naturalday(fecha)


def ultimo_sorteojugado(request):
    # Obtener el último registro
    # El primero en orden descendente es el último
    ultimo_sorteo = NumeroSorteados.objects.first()
    print(ultimo_sorteo)
    # Ahora puedes utilizar 'ultimo_registro' en tu plantilla o vista
    return render(request, 'lottoluck/daskboard.html', {'ultimo_sorteo': ultimo_sorteo})


@login_required
def venta_Numeros(request):
    year = datetime.datetime.now().year
    search_query = request.GET.get('search', '')
    # Search Query para la Busqueda Principal de la pagna princial
    if 'q' in request.GET:
        q = request.GET['q']
        numeroObjet = Numero.objects.filter(numero__icontains=q)
        numeros = Numero.objects.filter(numero__icontains=q)
    else:
        numeroObjet = Numero.objects.all().order_by('numero')
        numeros = Numero.objects.filter(numero__icontains=search_query)

    # Filtrar la lista de clientes en función del valor de búsqueda
    numeros = Numero.objects.filter(numero__icontains=search_query)
    elementos_por_pagina = 20
    # Show 10 clientes per page.
    paginator = Paginator(numeroObjet, elementos_por_pagina)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Obtiene la página actual de acuerdo al número de página proporcionado
    page = paginator.get_page(page_number)
    # Obtén el enlace al PDF
    pdf_link = None
    # Obtén el enlace al PDF

    try:
        # Obtén el último registro de VtasSorteo (puedes ajustar esto según tu lógica)
        ultimo_registro = VtasSorteo.objects.latest('id')
        # Genera el enlace al PDF utilizando el ID del último registro
        pdf_link = f'/descargar_pdf/{ultimo_registro.id}/'
    except VtasSorteo.DoesNotExist:
        # No se encontraron registros de VtasSorteo
        pass
    context = {
        'numeros': numeroObjet,  # Pasa la lista filtrada de clientes al contexto
        'search_query': search_query,
        'year': year,
        "page_obj": page_obj, 'pdf_link': pdf_link
    }

    return render(request, 'lottoLuck/ventas_numero.html', context)


@login_required
def ventaSorteo(request):
    year = datetime.datetime.now().year
    search_query = request.GET.get('search', '')
    # Search Query para la Busqueda Principal de la pagna princial
    if 'q' in request.GET:
        q = request.GET['q']
        numeroObjet = ventaSorteo.objects.all
        numeros = VtasSorteo.objects.all
    else:
        numeroObjet = VtasSorteo.objects.all()
        numeros = VtasSorteo.objects.all()

    # Filtrar la lista de clientes en función del valor de búsqueda
    numeros = VtasSorteo.objects.all
    elementos_por_pagina = 20
    # Show 10 clientes per page.
    paginator = Paginator(numeroObjet, elementos_por_pagina)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Obtiene la página actual de acuerdo al número de página proporcionado
    page = paginator.get_page(page_number)
    # Obtén el enlace al PDF
    pdf_link = None
    # Obtén el enlace al PDF

    try:
        # Obtén el último registro de VtasSorteo (puedes ajustar esto según tu lógica)
        ultimo_registro = VtasSorteo.objects.latest('id')
        # Genera el enlace al PDF utilizando el ID del último registro
        pdf_link = f'/descargar_pdf/{ultimo_registro.id}/'
    except VtasSorteo.DoesNotExist:
        # No se encontraron registros de VtasSorteo
        pass
    context = {
        'numeros': numeroObjet,  # Pasa la lista filtrada de clientes al contexto
        'search_query': search_query,
        'year': year,
        "page_obj": page_obj, 'pdf_link': pdf_link
    }

    return render(request, 'lottoLuck/ventasorteo.html', context)


def descargar_pdf(request, vtas_sorteo_id):
    vtas_sorteo = get_object_or_404(VtasSorteo, id=vtas_sorteo_id)
    # Suponiendo que 'pdf_file' es el campo en el modelo VtasSorteo que almacena el PDF
    pdf_file = vtas_sorteo.pdf_file

    response = FileResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{vtas_sorteo_id}.pdf"'
    return response


def cargar(request):
    year = datetime.datetime.now().year
    search_query = request.GET.get('search', '')
    # Search Query para la Busqueda Principal de la pagna princial
    if 'q' in request.GET:
        q = request.GET['q']
        numeroObjet = Numero.objects.filter(numero__icontains=q)
        numeros = Numero.objects.filter(numero__icontains=q)
    else:
        numeroObjet = Numero.objects.all().order_by('numero')
        numeros = Numero.objects.filter(numero__icontains=search_query)

    # Filtrar la lista de clientes en función del valor de búsqueda
    numeros = Numero.objects.filter(numero__icontains=search_query)
    elementos_por_pagina = 10
    # Show 10 clientes per page.
    paginator = Paginator(numeroObjet, elementos_por_pagina)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Obtiene la página actual de acuerdo al número de página proporcionado
    page = paginator.get_page(page_number)
    context = {
        'numeros': numeroObjet,  # Pasa la lista filtrada de clientes al contexto
        'search_query': search_query,
        'year': year,
        "page_obj": page_obj,
    }
    return render(request, 'lottoLuck/ventas_numero.html', context)


def agregar_numero(request, numero_id, desdecatalogo):

    micantidad = request.GET.get('cantidad')

    if micantidad is not None:
        micantidad = int(micantidad)
    else:
        micantidad = 1

    carrito = Carrito(request)
    numero = Numero.objects.get(id=numero_id)
    carrito.agregar(numero, micantidad)
    # Ordenar el carrito por producto_id
    carrito_ordenado = sorted(carrito.carrito.values(),
                              key=lambda x: x['nombre'])
    print('agrego:', numero_id, micantidad)
   # return redirect('venta_Numeros')
    if desdecatalogo == 1:
        return redirect('venta_Numeros')
    else:
        return render(request,  'lottoLuck/carrito.html')
    # return render(request, 'lottoLuck/carrito.html', {'carrito': carrito_ordenado})


def eliminar_numero(request, numero_id):
    carrito = Carrito(request)
    numero = Numero.objects.get(id=numero_id)
    carrito.eliminar(numero)
    return render(request,  'lottoLuck/carrito.html')


def restar_numero(request, numero_id):
    carrito = Carrito(request)
    numero = Numero.objects.get(id=numero_id)
    carrito.restar(numero)
    return render(request,  'lottoLuck/carrito.html')


def limpiar_numero(request):
    carrito = Carrito(request)
    carrito.limpiar()
    return render(request, 'lottoLuck/carrito.html')


def ver_carrito(request):
    carrito = Carrito(request)
    carrito_ordenado = sorted(carrito.carrito.values(),
                              key=lambda x: x['nombre'])
    clientes = None  # Inicializa la variable de clientes como None

    context = {
        'carrito': carrito_ordenado}

    return render(request, 'lottoLuck/carrito.html', context)


def listapdf(request, pdf_content):
    # Obtén el contenido HTML del contexto
    # pdf_content = request.GET.get('pdf_content', '')
    print(pdf_content)
    # Crea un objeto HTML a partir del contenido HTML
    html = HTML(string=pdf_content)

    # Genera el PDF
    pdf = html.write_pdf()

    # Crea una respuesta HTTP para descargar el PDF
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="reporte.pdf"'


def enviar_correo_con_pdf(pdf_buffer, destinatario, fileFactura, memo2, documento):
    # Configura las credenciales del servidor SMTP
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD
    print('smtp_username', smtp_username)
    # print('smtp_password', smtp_password)
    print('smtp_server', smtp_server)
    print('smtp_port', smtp_port)
    # Configura el mensaje de correo electrónico
    mensaje = MIMEMultipart()
    mensaje['From'] = smtp_username
    mensaje['To'] = destinatario
    mensaje['Subject'] = f' Su compra en LottoLuck No. {documento}'

    # Agrega el cuerpo del mensaje (opcional)
    mensaje.attach(
        MIMEText(memo2, 'plain'))

    # Adjunta el PDF al correo electrónico
    # Asegúrate de que el cursor del archivo esté al principio
    pdf_buffer.seek(0)
    pdf_attachment = MIMEApplication(pdf_buffer.read())
    pdf_attachment.add_header('Content-Disposition',
                              'attachment', filename=fileFactura)
    mensaje.attach(pdf_attachment)

    # Establece una conexión segura con el servidor SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Envía el correo electrónico
    server.sendmail(smtp_username, destinatario, mensaje.as_string())

    # Cierra la conexión con el servidor SMTP
    server.quit()


def generar_ticket_pdf(request):
    carrito = Carrito(request)
    carrito_ordenado = sorted(carrito.carrito.values(),
                              key=lambda x: x['nombre'])
    buffer = BytesIO()

    if request.method == 'POST':
        sorteovendedor = sorteo_vendedor_form(request.POST)
        cliente_seleccion_form = ClienteSeleccionForm(request.POST)
        fechavalidaform = fechaValidaSorteoForm(request.POST)
        JS = request.POST.get('tiposorteo')
        if sorteovendedor.is_valid():
            tiposorteo = request.POST.get('tiposorteo', 'SN')
            id_sorteo = request.POST.get('tiposorteo')
            id_sorteo = Sorteos.objects.get(pk=id_sorteo)
            sorteoName = id_sorteo.descripcion

            vendedor = request.POST.get('vendedor', 'CASA')
            vendedor_id = request.POST.get('vendedor')
            vendedor_db = Vendedor.objects.get(pk=vendedor_id)
            vendedorName = vendedor_db.nombre

            fechavalida = request.POST.get('fecha_valida', 'SF')

            if fechavalida and fechavalida != 'SF':
                try:
                    fecha = date_parser.parse(fechavalida)
                    fecha_palabras = fecha.strftime(
                        "%d de %B de %Y")  # Formatea la fecha
                except ValueError:
                    fecha_palabras = fechavalida
            else:
                fecha_palabras = fechavalida

            cliente_id = request.POST.get('opciones')
            cliente = Clientes.objects.get(pk=cliente_id)

            # Ahora puedes acceder a los atributos del cliente, como nombre, cédula, etc.
            nombre_cliente = cliente.nombre
            cedula_cliente = cliente.cedula
            email_cliente = cliente.email
            celular_cliente = cliente.telefono

            nombre1 = "ID:"+cliente_id + "-Cedula:" + cedula_cliente
            nombre2 = cliente.apellido+","+nombre_cliente

            print('JSERRANO__>', tiposorteo)
            print('Valor sorteo', vendedor)
            if tiposorteo is None or vendedor is None:
                vendedor = "Nulo"
                tiposorteo = "Nulo"
            # Aquí, estamos obteniendo la primera instancia de Secuencia
            secuencia = Secuencia.objects.first()
            memo = ''
            if secuencia:
                # numero_consecutivo1 = secuencia.numero_consecutivo
                numero_consecutivo = secuencia.incrementar_consecutivo()
                numero_consecutivo = str(secuencia.numero_consecutivo)

                # Configura el tamaño del papel similar al formato de ticket de rollo 80 mm
                width, height = 227, 1000  # Ancho y alto en unidades de mm
                # p = canvas.Canvas(buffer, pagesize=landscape((width, height)))
                p = canvas.Canvas(buffer, pagesize=(width, height))

                p.setFont("Helvetica-Bold", 8)
                barcode_value = f"{numero_consecutivo}"
                memo = memo+barcode_value + " \n"

                barcode = code128.Code128(
                    barcode_value, barHeight=18, humanReadable=True)
                # BarCode
                barcode_image = barcode.drawOn(p, 30, height - 45)
                # QR
                p.drawImage(barcode_image, 20, height - 50)

                # Agregar la imagen del código de barras al PDF

                p.setFont("Helvetica", 12)
                p.setFont("Helvetica-Bold", 16)
                p.drawString(20, height - 19, "LottoLuck")
                p.setFont("Helvetica", 7)
                p.drawString(10, height - 60, "Vendido a: "+nombre1)
                p.drawString(10, height - 70, " "+nombre2)

                p.drawString(10, height - 80, "Tipo de Sorteo: " + sorteoName)
                p.drawString(10, height - 90,
                             "Fecha Valida :" + fecha_palabras)
                # Establecer el color de fondo (verde)
                p.setFillColor(colors.green)
                # Configurar el color del trazo (borde) como transparente
                p.setStrokeColor(colors.transparent)
                p.rect(10, height - 110, 120, 12, fill=True)
                memo = memo + sorteoName+" \n"
                memo = memo+nombre1+" \n"+nombre2+"\n"
                memo = memo+fecha_palabras+" \n"

                # Establecer el color del texto (blanco)
                p.setFillColor(colors.white)

                p.drawString(10, height - 105,
                             "Articulo    Cant./Precio      TOTAL")

                # ...

                # Asegúrate de que el color vuelva a su valor original después de imprimir el encabezado
                p.setFillColor(colors.black)

                y_position = height - 107
                p.setFont("Helvetica-Bold", 6)
                for item in carrito_ordenado:
                    y_position -= 10
                    nombre = item['nombre']
                    cantidad = item['cantidad']
                    precio = item['precio']
                    acumulado = item['acumulado']

                # Formatear los valores como cadenas
                    cantidad_str = str(cantidad)
                    precio_str = f"${precio:0.2f}"
                    acumulado_str = f"${acumulado:0.2f}"

                    # Ajusta la longitud fija de las cadenas
                    nombre = nombre.ljust(20)  # Ajusta la longitud deseada
                    cantidad_str = cantidad_str.ljust(
                        10)  # Ajusta la longitud deseada
                    # Ajusta la longitud deseada
                    precio_str = precio_str.ljust(10)
                    acumulado_str = acumulado_str.ljust(
                        10)  # Ajusta la longitud deseada

                    # Concatenar la información y agregarla al PDF
                    item_info = f"{nombre} {cantidad_str} * {precio_str} {acumulado_str}"
                    memo = memo+item_info+" \n"
                    p.drawString(10, y_position, item_info)

                # Calcular el total y agregarlo al PDF
                y_position -= 10
                totalCompra = total_compra(request)['total_compra']
                total_str = f"Total: ${totalCompra:0.2f}"
                y_position -= 10
                memo = memo+total_str+" \n"

                p.setFont("Helvetica-Bold", 15)
                p.drawString(10, y_position, total_str)

                totalqty = total_qty(request)['total_qty']
                total_str = f"Cant.Comprada:{totalqty:0.0f}"
                memo = memo+total_str+" \n"
                y_position -= 10
                p.setFont("Helvetica", 8)
                p.drawString(10, y_position, total_str)

                totallinea = total_linea(request)['total_linea']
                total_str = f"Total Items:{totallinea:0.0f}"
                memo = memo+total_str+" \n"
                y_position -= 10
                p.setFont("Helvetica", 8)
                p.drawString(10, y_position, total_str)

                # Agregar el campo 'Vendedor' al PDF
                p.setFont("Helvetica", 6)
                vendedor_str = "Vendedor: " + vendedorName
                y_position -= 10
                memo = memo+vendedor_str+" \n"
                p.drawString(10, y_position, vendedor_str)
                vendedor_str = "Firma:_______________________ "
                y_position -= 10
                p.drawString(10, y_position, vendedor_str)
                vendedor_str = "Recibido:____________________ "
                y_position -= 10
                p.drawString(10, y_position, vendedor_str)

                # ...

                # Obtener la fecha y hora actual
                fecha_hora_actual = arrow.now().format("YYYY-MM-DD HH:mm:ss")
                memo = memo+fecha_hora_actual+" \n"

                # Imprimir la fecha y hora en el PDF
                p.setFont("Helvetica", 7)
                y_position -= 10
                p.drawString(10, y_position,
                             f"**Procesado:{fecha_hora_actual} **")

                # Guardar el PDF en el buffer y cerrar el objeto Canvas
                p.showPage()
                p.save()
                buffer.seek(0)
                # secuencia.incrementar_consecutivo()
                # Crear una respuesta de tipo FileResponse
                response = FileResponse(buffer, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="ticket.pdf"'

                # guarda los daros de ventas:
                # Crear una instancia de VtasSorteo para almacenar los datos de la venta
                vtas_sorteo = VtasSorteo(
                    id_sorteo=id_sorteo,
                    fecha_sorteo=fechavalida,          # Sustituye con la fecha correcta
                    totalventa=totalCompra,             # Sustituye con el total de la venta
                    totalqty=totalqty,                  # Sustituye con la cantidad comprada
                    monto_premio1=0.0,                  # Sustituye con el monto correcto
                    monto_premio2=0.0,                  # Sustituye con el monto correcto
                    monto_premio3=0.0,                  # Sustituye con el monto correcto
                    # Sustituye con el ID correcto del vendedor
                    id_vendedor=vendedor_db,
                    id_cliente=cliente,                 # Asigna la instancia del cliente
                    transaction_id=numero_consecutivo,  # Sustituye con el ID de transacción correcto
                    descripcion=memo,                   # Sustituye con la descripción correcta
                    estado="Facturado"                 # Sustituye con el estado correcto

                )
                # Guardar el archivo PDF en el campo pdf_file
                filefactura = "cedula-"+cedula_cliente + \
                    "-"+str(numero_consecutivo)+".pdf"
                vtas_sorteo.pdf_file.save(filefactura, File(buffer))

                vtas_sorteo.save()

                # Itera a través de los elementos del carrito y crea instancias de VtasDetalle
                for item in carrito_ordenado:
                    nombre = item['nombre']
                    cantidad = item['cantidad']
                    precio = item['precio']
                    acumulado = item['acumulado']
                    # Asegúrate de tener el número correcto
                    numero = nombre

                    # Crea una instancia de VtasDetalle para cada elemento en el carrito
                    vtas_detalle = VtasDetalle(
                        id_vtasorteo=vtas_sorteo,   # Asigna la instancia de VtasSorteo creada anteriormente
                        id_sorteo=id_sorteo,
                        cantidad=cantidad,
                        fecha_sorteo=fechavalida,
                        numero=numero,               # Asigna el número correcto
                        total=acumulado,            # Asigna el total acumulado
                        ganador_1=False,            # Inicialmente, no se sabe si es ganador
                        ganador_2=False,
                        ganador_3=False
                    )
                    vtas_detalle.save()
                limpiar_numero(request)
                venta_Numeros(request)
                # Mensaje de notificación
                messages.success(
                    request, f'Su Factura:{filefactura} se ha generado correctamente.')

                # Envía el correo electrónico con el PDF adjunto
                # Revisar el tema de Gmail.../zohoMail

                comprador = f"Sr/Sra , {nombre2}"+"\n"
                comprador = comprador + \
                    f"Gracias por su Compra en lottoluck valido para  {fecha_palabras}.\n"
                comprador = comprador + \
                    f"Usted realizo la compra para el sorteo: {sorteoName}, Ticket No.{numero_consecutivo}.\n"
                if email_cliente:
                    try:
                        enviar_correo_con_pdf(
                            buffer, email_cliente, filefactura, comprador, numero_consecutivo)
                    except Exception as e:
                        # Maneja la excepción de la función de envío de WhatsApp aquí
                        # Por ejemplo, puedes imprimir un mensaje de error en el registro de Django
                        print(f"Error al enviar mensaje de Email : {str(e)}")
                    messages.success(
                        request, f'Factura:{filefactura} se envio a: {email_cliente}')
                if celular_cliente:
                    # Llamada a la función para enviar mensaje de WhatsApp
                    try:
                        enviar_mensaje_whatsapp(
                            numero_consecutivo, filefactura, comprador, celular_cliente)
                    except Exception as e:
                        # Maneja la excepción de la función de envío de WhatsApp aquí
                        # Por ejemplo, puedes imprimir un mensaje de error en el registro de Django
                        print(f"Error al enviar mensaje de WhatsApp: {str(e)}")

                    messages.success(
                        request, f'Factura:{filefactura} enviada SMS/WhatSapp:{celular_cliente}')

                    # enviar_mensaje_whatsapp2(request)
                # Redirección después de mostrar el mensaje
                return redirect('venta_Numeros')

            else:
                sorteovendedor = sorteo_vendedor_form()
                cliente_seleccion_form = ClienteSeleccionForm()

    response = FileResponse(buffer, content_type='application/pdf')

    return response


def enviar_mensaje_whatsapp2(request):
    import nexmo  # Para Nexmo o import sinchsms  # Para Sinch, dependiendo de cuál estés utilizando
    NEXMO_API_KEY = 'gbZA3UsvERXAEg1J'
    NEXMO_API_SECRET = 'xwdttbPrYZUDSfulTvOZOtLD6HaBBQ0i5lpn9iuEpReMZ0wmUct'

    if request.method == 'POST':
        # Número de WhatsApp al que deseas enviar el mensaje
        numero_destino = '66194728'
        mensaje = 'Este es tu mensaje de prueba desde Django'  # Contenido del mensaje

        # Inicializa el cliente de Nexmo o Sinch
        client = nexmo.Client(api_key=NEXMO_API_KEY,
                              api_secret=NEXMO_API_SECRET)
        # O para Sinch:
        # client = sinchsms.SinchSMS(SINCH_APP_KEY, SINCH_APP_SECRET)

        try:
            # Envía el mensaje de WhatsApp
            response = client.send_message({
                'from': '66194728',  # Tu número de WhatsApp registrado
                'to': numero_destino,
                'text': mensaje
            })

            # Verifica si el mensaje se envió con éxito
            if response['messages'][0]['status'] == '0':
                return HttpResponse('Mensaje de WhatsApp enviado con éxito')
            else:
                return HttpResponse('Error al enviar el mensaje de WhatsApp')

        except Exception as e:
            return HttpResponse(f'Error: {str(e)}')

    return render(request, 'tu_template.html')


def enviar_mensaje_whatsapp(numero_consecutivo, filefactura, nombre2, telefono_cliente):
    # Configura el cliente de Twilio
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    # Construye el enlace al PDF
    pdf_url = reverse('descargar_pdf', args=[numero_consecutivo])

    # Construye el mensaje de WhatsApp
    mensaje = f"Hola {nombre2}!\n"
    mensaje += f"Su factura {filefactura} ha sido generada con éxito.\n"
    mensaje += f"Puede descargarla aquí: {pdf_url}"

    # Envia el mensaje a través de Twilio
    message = client.messages.create(
        body=mensaje,
        from_=settings.TWILIO_PHONE_NUMBER,
        to=telefono_cliente
    )

    # Verifica el estado del mensaje y muestra un mensaje en la consola
    if message.sid:
        print(f"Mensaje enviado a {telefono_cliente} con éxito.")
    else:

        print("Error al enviar el mensaje de WhatsApp.")


def detalle_cliente_y_ticket(request, numero, id_sorteo, fecha_sorteo):
    clientes_tickets = VtasDetalle.get_clientes_y_tickets_de_compra(
        numero, id_sorteo, fecha_sorteo)
    if clientes_tickets:
        context = {
            'numero': numero,
            'clientes_tickets': clientes_tickets,
        }
        return render(request, 'lottoLuck/cliente_detalle.html', context)
    else:
        # Manejo de caso en el que no se encontró ningún registro
        context = {
            'mensaje': 'No se encontró ningún registro con los parámetros proporcionados.',
        }
        return render(request, 'lottoLuck/error.html', context)


def compradoresdelNumero(request, numero_id):
    # return render(request,  'lottoLuck/consultasorteo.html')
    numero = numero_id  # Reemplaza con el número que deseas buscar
    id_sorteo = 1  # Reemplaza con el ID del sorteo que deseas buscar
    fecha_sorteo = '2023-10-22'  # Reemplaza con la fecha que deseas buscar

    resultado = VtasDetalle.get_cliente_y_ticket_de_compra(
        numero, id_sorteo, fecha_sorteo)

    if resultado:
        print("Detalle del Cliente:")
        print(f"Nombre: {resultado['cliente']['nombre']}")
        print(f"Cédula: {resultado['cliente']['cedula']}")
        print(f"Dirección: {resultado['cliente']['direccion']}")
        print(f"Email: {resultado['cliente']['email']}")
        print(f"Teléfono: {resultado['cliente']['telefono']}")
        print("\nDetalle del Ticket de Compra:")
        print(f"ID del Ticket: {resultado['ticket_de_compra']['id']}")
        print(
            f"Fecha del Sorteo: {resultado['ticket_de_compra']['fecha_sorteo']}")
        print(f"Descripción: {resultado['ticket_de_compra']['descripcion']}")
        print(f"Estado: {resultado['ticket_de_compra']['estado']}")
    else:
        print("No se encontró ningún registro con los parámetros proporcionados.")
    return redirect('consultasorteo')


def consultasorteo(request):
    if request.method == 'POST':
        fechasorteo = fechaSorteoForm(request.POST)
        if fechasorteo.is_valid():
            id_sorteo = request.POST.get('tiposorteo')
            id_sorteo = Sorteos.objects.get(pk=id_sorteo)
            sorteoName = id_sorteo.descripcion
            pago1 = id_sorteo.paga1
            pago2 = id_sorteo.paga2
            pago3 = id_sorteo.paga3
            fechavalida = request.POST.get('fecha_valida')

            resultados = VtasSorteo.get_totalventas_and_totalqty(
                id_sorteo, fechavalida)

            totalventa = resultados['totalventa']
            totalqty = resultados['totalqty']

            numeroitems = VtasDetalle.count_sales_items(id_sorteo, fechavalida)

            resumen = VtasDetalle.get_sales_summary(id_sorteo, fechavalida)
            resumen = [item.split(', ') for item in resumen]
            resumen_con_premios = []
            resumen_expandido = []
            # Premios para los que se multiplicará
            premios = [pago1, pago2, pago3]
            # Itera sobre los elementos de resumen
            for item in resumen:
                numero = item[0]
                cantidad = int(item[1])
                monto = Decimal(item[2])  # Convertir monto a Decimal

                # Lista para almacenar los resultados para este elemento
                resultados_elemento = [numero, cantidad, str(monto)]

                # Multiplica por cada premio y agrega los resultados
                for premio in premios:
                    resultado_premio = cantidad * premio
                    resultados_elemento.append(str(resultado_premio))

                # Agrega los resultados al resumen_expandido

                resumen_expandido.append(resultados_elemento)
            print('resumen3', resumen_expandido)
            print('total items:', numeroitems)
            context = {
                'fechasorteo': fechasorteo,
                'id_sorteo': id_sorteo,
                'fecha': fechavalida,
                'totalventa': totalventa,
                'totalqty': totalqty,
                'resumen': resumen_expandido,
                'numeroitems': numeroitems

            }
            # Renderiza el contenido de consultasorteo.html a una cadena HTML

            return render(request, 'lottoluck/consultasorteo.html', context)

    else:
        fechasorteo = fechaSorteoForm()  # Pasa el contexto a la vista que generará el PDF
        context = {
            'fechasorteo': fechasorteo, }

        # Renderiza el contenido de consultasorteo.html a una cadena HTML

    return render(request, 'lottoluck/consultasorteo.html', context)


def consultar_cliente(request):
    if request.method == 'POST':
        form = ConsultaClienteForm(request.POST)
        fechavalidaform = fechaValidaSorteoForm(request.POST)

        # Crear el formulario de selección de cliente
        cliente = None
        cedula_o_nombre = None
        print('que hay aqui:', cedula_o_nombre)
        if form.is_valid():
            cedula_o_nombre = form.cleaned_data['cedula_o_nombre']
            print(cedula_o_nombre)
            if len(cedula_o_nombre) > 0:
                cliente_seleccion_form = ClienteSeleccionForm()

            # Realizar una búsqueda con el operador Q para buscar por cédula o nombre
            clientes = Clientes.objects.filter(
                Q(cedula__iexact=cedula_o_nombre) | Q(nombre__iexact=cedula_o_nombre))
            if clientes:
                print("cedula_o_nombre:", cedula_o_nombre)

                opciones = [
                    (cliente.id, f"Cédula: {cliente.cedula} - {cliente.nombre} {cliente.apellido}  - {cliente.id} -Correo:{cliente.email}") for cliente in clientes]

                cliente_seleccion_form.fields['opciones'].choices = opciones
                print("opciones:", opciones)

                # cliente_id = request.POST.get('opciones')
                # Usar get_object_or_404 en lugar de get
                # cliente = get_object_or_404(Clientes, pk=cliente_id)

                # cliente = Clientes.objects.get(pk=cliente_id)
        else:
            # Instancia el formulario incluso si hay un error en form
            cliente_seleccion_form = ClienteSeleccionForm()
            # Ahora puedes acceder a los atributos del cliente, como nombre, cédula, etc.
        sorteovendedor = sorteo_vendedor_form()
        return render(request, 'lottoluck/pagar.html', {'consulta_form': form,
                                                        'cliente_seleccion_form': cliente_seleccion_form,
                                                        'sorteovendedor': sorteovendedor,
                                                        'fechavalidaform': fechavalidaform,
                                                        'clienteObjeto': cliente
                                                        })
    else:
        sorteovendedor = sorteo_vendedor_form()
        form = ConsultaClienteForm()
        fechavalidaform = fechaValidaSorteoForm()

        # Crea una instancia del formulario de selección de cliente
        cliente_seleccion_form = ClienteSeleccionForm()
    return render(request, 'lottoluck/pagar.html', {'consulta_form': form,
                                                    'cliente_seleccion_form': cliente_seleccion_form,
                                                    'sorteovendedor': sorteovendedor,
                                                    'fechavalidaform': fechavalidaform})


def pagar(request):
    carrito = Carrito(request)
    carrito_ordenado = sorted(carrito.carrito.values(),
                              key=lambda x: x['nombre'])

    if request.method == 'POST':
        form = ConsultaClienteForm(request.POST)
        # Crear el formulario de selección de cliente
        cliente_seleccion_form = ClienteSeleccionForm()

        if form.is_valid():
            cedula_o_nombre = form.cleaned_data['cedula_o_nombre']

            # Realizar una búsqueda con el operador Q para buscar por cédula o nombre
            clientes = Clientes.objects.filter(
                Q(cedula__iexact=cedula_o_nombre) | Q(nombre__iexact=cedula_o_nombre))

            if clientes:
                opciones = [
                    (cliente.id, f"Cédula: {cliente.cedula} - {cliente.nombre} {cliente.apellido}  - {cliente.id} ") for cliente in clientes]
                cliente_seleccion_form.fields['opciones'].choices = opciones
        else:
            # Instancia el formulario incluso si hay un error en form
            cliente_seleccion_form = ClienteSeleccionForm()
        sorteos_form = SorteosForm(request.POST)
        vendedor_forma = VendedorForm(request.POST)
    else:
        form = ConsultaClienteForm()
        cliente_seleccion_form = ClienteSeleccionForm()
        sorteos_form = SorteosForm()
        vendedor_forma = VendedorForm()
    context = {
        'carrito': carrito_ordenado,
        'consulta_form': form,
        'cliente_seleccion_form': cliente_seleccion_form,
        'sorteos_form': sorteos_form,
        'vendedor_forma': vendedor_forma
    }

    return render(request, 'lottoluck/pagar.html', context)


def contadores(request):
    # Cuenta la cantidad de clientes en la base de datos
    cantidad_clientes = Clientes.objects.count()
    cantidad_vendedores = Vendedor.objects.count()
    cantidad_sorteo = Sorteos.objects.count()
    cantidad_casag = Casagrande.objects.count()
    # Obtén la cantidad de registros en VtasSorteo
    cantidad_vtasorteo = VtasSorteo.objects.count()
    conteo_diferentes_id_sorteo = VtasSorteo.objects.values(
        'id_sorteo').distinct().count()

    # El primero en orden descendente es el último
    ultimo_sorteo = NumeroSorteados.objects.first()
    numero = ultimo_sorteo.referencia
    fecha = ultimo_sorteo.fecha
    letra = ultimo_sorteo.get_letras()
    elJson = ultimo_sorteo.toJSON()
    contexto = {
        'ctes': cantidad_clientes,
        'vend': cantidad_vendedores,
        'sorteo': cantidad_sorteo,
        'casag': cantidad_casag,
        'ventas': cantidad_vtasorteo,
        'SorteoEnVenta': conteo_diferentes_id_sorteo,
        'numero': numero,
        'fecha': fecha,
        'letra': letra,
        'myjson': elJson,
    }
    print(elJson)
    print("Total clientes:", cantidad_clientes)
    print("Total vendedores:", cantidad_vendedores)
    print("Total tipoSorteo:", cantidad_sorteo)
    print("Total casaGrande:", cantidad_casag)
    print("Numero", numero)
    print("fecha", fecha)
    return render(request, 'lottoluck/daskboard.html',  contexto)


def borrar_cliente(request, cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)

    if request.method == 'POST':
        cliente.delete()
        # Redirige a la lista de clientes después de eliminar
        return redirect('lista_clientes')
    else:
        context = {
            'cliente': cliente,
        }
        return render(request, 'lottoLuck/borrar_cliente.html', context)


@login_required
def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Clientes, id=cliente_id)

    if request.method == 'POST':
        # form = ClienteEditForm(request.POST, instance=cliente)

        form = ClienteEditForm(request.POST, request.FILES, instance=cliente)
        print(form)
        if form.is_valid():
            form.save()
            # Redirige a la lista de clientes después de editar
            return redirect('lista_clientes')
        else:
            # Manejo de errores de validación: volver a mostrar el formulario con errores
            context = {
                'cliente': cliente,
                'form': form,
            }
            return render(request, 'lottoLuck/editar_clientes.html', context)
    else:
        form = ClienteEditForm(instance=cliente)

    context = {
        'cliente': cliente,
        'form': form,
    }

    return render(request, 'lottoLuck/editar_clientes.html', context)


class ClientesListView(ListView):
    model = Clientes
    template_name = 'lottolLuck/clientes_list.html'  # Nombre de tu plantilla HTML
    context_object_name = 'clientes'  # Nombre de la variable en el contexto
    paginate_by = 10  # Número de elementos por página

    def get_queryset(self):
        # Obtén el valor de búsqueda desde la URL (query parameter)
        search_query = self.request.GET.get('q')

        if search_query:
            # Filtra los clientes por nombre o cualquier otro campo relevante
            return Clientes.objects.filter(
                Q(nombre__icontains=search_query) |  # Búsqueda por nombre
                Q(apellido__icontains=search_query) |  # Búsqueda por apellido
                # Búsqueda por email u otros campos
                Q(email__icontains=search_query)
            )

        # Si no hay consulta de búsqueda, muestra todos los clientes

        return Clientes.objects.all()


@login_required
def lista_clientes(request):
    year = datetime.datetime.now().year
    # Obtener el valor de búsqueda del formulario
    search_query = request.GET.get('search', '')
    # Search Query para la Busqueda Principal de la pagna princial
    if 'q' in request.GET:
        q = request.GET['q']
        clienteObjet = Clientes.objects.filter(nombre__icontains=q)
        clientes = Clientes.objects.filter(nombre__icontains=q)
    else:
        clienteObjet = Clientes.objects.all()
        clientes = Clientes.objects.filter(nombre__icontains=search_query)

    # Filtrar la lista de clientes en función del valor de búsqueda
    clientes = Clientes.objects.filter(nombre__icontains=search_query)

    elementos_por_pagina = 10
    # Show 10 clientes per page.
    paginator = Paginator(clienteObjet, elementos_por_pagina)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # Obtiene la página actual de acuerdo al número de página proporcionado
    page = paginator.get_page(page_number)

    context = {
        'clientes': clienteObjet,  # Pasa la lista filtrada de clientes al contexto
        'search_query': search_query,
        'year': year,
        "page_obj": page_obj,

    }
    # print(clientes)
    return render(request, 'lottoLuck/lista_clientes.html', context)


def add_cliente(request):
    data = {
        'form': ClienteForm
    }
    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Cliente Adicionado"
        else:
            data['form'] = formulario

        return redirect('lista_clientes')
    return render(request, 'lottoLuck/add_cliente.html', data)
# views.py


def add_cliente1(request):
    if request.method == 'POST':
        # Obtiene los datos del formulario
        cedula = request.POST['cedula']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']

        # Crea un nuevo cliente
        cliente = Clientes(cedula=cedula, nombre=nombre, apellido=apellido)
        cliente.save()

        # Redirige a la página de clientes o a donde desees
        return redirect('lista_clientes')
    return render(request, 'lottoLuck/add_cliente.html')
# views.py
# Create your views here.


def is_admin(user):
    return user.is_authenticated and user.is_superuser


@login_required
@user_passes_test(is_admin)
def init_numeros(request):
    # Elimina todos los registros existentes en la tabla Numeros
    from .models import Numero
    # Numero.objects.all().delete()

    # Crea números del 00 al 99 y guárdalos en la tabla Numeros
    for numero in range(100):
        # Convierte el número en una cadena de dos dígitos (rellena con ceros)
        numero_str = f'{numero:02}'
    #   Numero.objects.create(id=numero_str, numero=numero_str,
    #                          limite=9999, activo=True, imagen=None, url=None)

    return HttpResponse("Tabla Numero inicializada correctamente")


def login_view(request):
    template_name = 'login.html'  # Ruta a tu plantilla de inicio de sesión personalizada
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Reemplaza 'tu_pagina_principal' con la URL a la que deseas redirigir después del inicio de sesión
            return redirect('lottoluck/')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    # Especifica el nombre de tu plantilla de
    template_name = 'lottoLuck/logout.html'
    # logout(request)
    return redirect('login')


def custom_logout(request):
    # Personaliza la lógica de cierre de sesión si es necesario
    logout(request)
    return HttpResponseRedirect(reverse('lottoLuck/logout.html'))


class CustomLogoutView(LogoutView):
    # Especifica el nombre de tu plantilla de cierre de sesión personalizada
    template_name = 'lottoLuck/logout.html'


@login_required
def generate_fake_clients(request):
    # Llama al comando personalizado 'generate_fake_clients'
    call_command('generate_fake_clients')
    return HttpResponse("Datos falsos generados con éxito.")


def editar_numero_sorteados(request, numero_sorteados_id):
    numero_sorteados = get_object_or_404(
        NumeroSorteados, id=numero_sorteados_id)
    if request.method == 'POST':
        form = NumeroSorteadosForm(request.POST, instance=numero_sorteados)
        print("paso POST")
        if form.is_valid():
            print("paso VALID")
            form.save()
            # Redirige a la lista de números sorteados
            return redirect('/')

        else:
            context = {
                'form': form,
            }
            print("NO paso POST")

        return render(request, 'lottoluck/editar_numero_sorteados.html', context)
    else:
        form = NumeroSorteadosForm(instance=numero_sorteados)
    context = {
        'form': form,
    }

    return render(request, 'lottoluck/editar_numero_sorteados.html',  context)


def agregar_numero_sorteados(request):
    data = {
        'form': NumeroSorteadosForm
    }
    if request.method == 'POST':
        form = NumeroSorteadosForm(data=request.POST)
        if form.is_valid():
            form.save()
            # Reemplaza 'ruta_de_redireccion' por la ruta a la que deseas redirigir después de la adición
            data['mensaje'] = "Sorteo creado"
            return redirect('lista_numero_sorteados')

        else:
            data['form'] = form
            return redirect('lista_numero_sorteados')
    return render(request, 'lottoluck/add_numero_sorteados.html', data)


def lista_numero_sorteados(request):
    numero_sorteados = NumeroSorteados.objects.all()
    print('Aqui 1:', numero_sorteados)
    if request.method == 'POST':
        form = NumeroSorteadosForm(instance=numero_sorteados)
        return render(request, 'lottoluck/editar_numero_sorteados.html', {'form': form, 'numero_sorteados': numero_sorteados})
    else:
        form = NumeroSorteadosForm()

    return render(request, 'lottoluck/lista_numero_sorteados.html', {'numeros_sorteados': numero_sorteados})


def get_items(request):
    items = ["Item 1", "Item 2", "Item 3"]
    return render(request, 'lottoluck/mytemplate.html', {'items': items})
    # return JsonResponse({'items': items})


def detalle_venta_ticket(request, transaction_id):
    venta = get_object_or_404(VtasSorteo, transaction_id=transaction_id)
    detalles = VtasDetalle.objects.filter(id_vtasorteo=venta)

    return render(request, 'lottoluck/detalle_venta_ticket.html', {'venta': venta, 'detalles': detalles})


def buscar_venta(request):
    if request.method == "POST":
        numero_ticket = request.POST.get('numero_ticket')
        try:
            venta = VtasSorteo.objects.get(transaction_id=numero_ticket)
            detalles = venta.vtasdetalles.all()  # Obtén los detalles relacionados
            return render(request, 'lottoluck/detalle_venta_ticket.html', {'venta': venta, 'detalles': detalles})
        except VtasSorteo.DoesNotExist:
            error_message = "Venta no encontrada."
            return render(request, 'lottoluck/detalle_venta_ticket.html', {'error_message': error_message})
    return render(request, 'lottoluck/detalle_venta_ticket.html')
