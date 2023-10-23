
import os

import inflect
from num2words import num2words
from datetime import date
from datetime import datetime
from django.db import models
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.forms import model_to_dict
from django.conf import settings
from django.contrib.auth.models import User

from django.db.models import Count, Sum, F

GENDER = (
    ('M', 'Masculino'),
    ('F', 'Femenino'),
)


class Casagrande(models.Model):
    # models.IntegerField(primary_key=True)
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=255, null=True, unique=True, verbose_name='nombre')
    direccion = models.CharField(
        max_length=255, null=True, verbose_name='Direccion')
    telefono = models.CharField(
        max_length=255,  null=True, verbose_name='Telefono')
    email = models.CharField(max_length=255, null=True, verbose_name='Correo')

    def __str__(self):
        return self.get_full_casagrande()

    def get_full_casagrande(self):
        return f'{self.id} - {self.nombre}'

    def get_short_name(self):
        return f'{self.nombre}'

    def toJSON(self):
        item = model_to_dict(self)
        # item['nombre'] = self.get_full_casagrande
        # item['direccion'] = self.direccion
        # item['email'] = self.email
        # item['telefono'] = self.telefono
        return item

    class Meta:
        verbose_name = 'Casagrande'
        verbose_name_plural = 'Casagrandes'


class Vendedor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(
        max_length=255, null=True, unique=True, verbose_name='nombre')
    id_casagrande = models.ForeignKey(
        'Casagrande', on_delete=models.PROTECT, verbose_name='id_CasaGrande')
    comision = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.00, verbose_name='% Comision')

    def __str__(self):
        return self.nombre

    def get_full_vendedor(self):
        return f'{self.id} - {self.nombre}'

    def toJSON2(self):
        item = model_to_dict(self)
        item['nombre'] = self.get_full_vendedor()
        item['direccion'] = self.direccion
        item['id_casagrande'] = self.Casagrande.toJSON()
        item['comision'] = str(self.comision)
        return item

    def to_json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            # Otros atributos relevantes
        }


class Sorteos(models.Model):
    id = models.AutoField(primary_key=True)
    descripcion = models.CharField(
        max_length=255, null=True, unique=True, verbose_name='Descripcion')
    costoporNumero = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.20, verbose_name='Costo por Numero')
    paga1 = models.DecimalField(
        max_digits=9, decimal_places=2, default=11.00, verbose_name='Pago_Primer Premio')
    paga2 = models.DecimalField(
        max_digits=9, decimal_places=2, default=3.00, verbose_name='Pago_Segundo Premio')
    paga3 = models.DecimalField(
        max_digits=9, decimal_places=2, default=2.00, verbose_name='Pago_Tercer  Premio')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.descripcion

    def to_json(self):
        return {
            'id': self.id,
            'descripcion': self.descripcion,
            # Otros atributos relevantes
        }

    def toJSON(self):
        item = model_to_dict(self)
        item['costoporNumero'] = self.valorNumero
        return item

    def valorNumero(self):
        return f'{self.costoporNumero}'

    class Meta:
        verbose_name = ' Sorteo'
        verbose_name_plural = ' Sorteo'

    @classmethod
    def __json_decode__(cls, data):
        # Reconstruct the object from the serialized data
        return cls.objects.get(id=data['id'])


tipo_cliente = [
    [0, "Regular"],
    [1, "Especial"],
    [2, "VIP"],
    [3, "Compra Credido"],
    [4, "Casa Grande"],
    [5, "Familiar"],
    [8, "Otros"]
]


class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
    cedula = models.CharField(max_length=16, null=True,
                              verbose_name='Cedula-Pasaporte')
    nombre = models.CharField(max_length=255, null=True, verbose_name='Nombre')
    apellido = models.CharField(
        max_length=255, null=True, verbose_name='Apellido')
    gender = models.CharField(
        max_length=50, choices=GENDER, default=GENDER[0][0], verbose_name='Genero')

    direccion = models.CharField(
        max_length=255, null=True, verbose_name='Direccion')
    email = models.EmailField(max_length=255, null=True, verbose_name="Correo")
    telefono = models.CharField(
        max_length=12, null=True, verbose_name='Celular')
    birthdate = models.DateField(
        default=datetime.now, verbose_name='Fecha de nacimiento')
    imagen = models.ImageField(upload_to='clientes', null=True, blank=True)
    # url = models.TextField(max_length=60,null=True,verbose_name='url')
    tipocliente = models.IntegerField(
        choices=tipo_cliente, default=0, verbose_name='Tipo Cliente')
    date_creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_full_name()

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def get_full_name(self):
        return f'{self.nombre}  {self.apellido}'

    def get_cedula(self):
        return f'{self.cedula}'

    def get_short_name(self):
        return f'{self.nombre}'

    def get_image(self):
        if self.imagen:
            return f'{settings.MEDIA_URL}{self.imagen}'
        return f'{settings.STATIC_URL}empty.png'

    @property
    def imageURL(self):
        try:
            url = self.imagen.url
        except:
            url = ''
        return url

    def toJSON(self):
        item = model_to_dict(self)
        item['nombre'] = self.get_full_name()
        item['apellido'] = self.get_short_name()
        item['cedula'] = self.get_cedula()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        item['direccion'] = self.direccion
        item['gender'] = {'id': self.gender, 'name': self.get_gender_display()}
        item['email'] = self.email
        item['telefono'] = self.telefono
        item['imagen'] = self.get_image()
       # item['url']= self.url
        return item

    class Meta:
        verbose_name = 'Clientes'
        verbose_name_plural = 'Clientes'


class NumeroSorteados(models.Model):
    id = models.AutoField(primary_key=True)
    id_sorteo = models.ForeignKey(
        'Sorteos', on_delete=models.PROTECT, verbose_name='tipo')
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha')
    referencia = models.CharField(
        max_length=30, null=True, verbose_name='#LNB')

    I_premio = models.DecimalField(
        max_digits=4, decimal_places=0, default=0, verbose_name='IPremio')
    letras = models.CharField(max_length=4, null=True, verbose_name="Letras")
    serie = models.CharField(max_length=2, null=True, verbose_name="Serie")
    folio = models.CharField(max_length=2, null=True, verbose_name="Folio")

    II_premio = models.DecimalField(
        max_digits=4, decimal_places=0, default=0, verbose_name='IIPremio')
    III_premio = models.DecimalField(
        max_digits=4, decimal_places=0, default=0, verbose_name='IIIPremio')

    # Campo creado automáticamente al crear un registro
    created_at = models.DateTimeField(auto_now_add=True)

    def get_primero(self):
        return f'{self.I_premio}'

    def get_letras(self):
        return f'{self.letras}'

    def get_serie(self):
        return f'{self.serie}'

    def get_folio(self):
        return f'{self.folio}'

    def get_segundo(self):
        return f'{self.II_premio}'

    def get_tercero(self):
        return f'{self.III_premio}'

    def fecha_sorteo2(self):
        return self.fecha.strftime('%d-%m-%Y')

    def fecha_sorteo2(self):
        meses = [
            'Enero', 'Febrero', 'Marzo', 'Abril',
            'Mayo', 'Junio', 'Julio', 'Agosto',
            'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
        ]
        dia = self.fecha.day
        # Restamos 1 para obtener el nombre del mes correcto
        mes = meses[self.fecha.month - 1]
        año = self.fecha.year
        return f'{dia} de {mes} de {año}'

    def get_nombre_sorteo(self):
        return self.id_sorteo.descripcion if self.id_sorteo else ""

    def toJSON(self):
        item = model_to_dict(self)
        item['I_premio'] = self.get_primero()
        item['letras'] = self.get_letras()
        item['serie'] = self.get_serie()
        item['folio'] = self.get_folio()
        item['II_premio'] = self.get_segundo()
        item['III_premio'] = self.get_tercero()
        item['fecha'] = self.fecha_sorteo2()
        item['referencia'] = self.referencia
        item['nombredelsorteo'] = self.get_nombre_sorteo()

        return item

    class Meta:
        # Ordenar por fecha de creación en orden descendente
        ordering = ['-created_at']


class Numero(models.Model):
    id = models.AutoField(primary_key=True)
    numero = models.CharField(max_length=2)
    costo = models.DecimalField(max_digits=10, decimal_places=2)
    limite = models.IntegerField(default=9999)
    activo = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='numeros', null=True, blank=True)

    def __str__(self):
        return self.numero

    @property
    def numero_a_palabra(self):
        # p = inflect.engine()
        # p.locale('es')  # Configura el idioma a español
        numero_ = self.numero
        # numero_en_palabras = p.number_to_words(int(numero_))
        # print(numero_en_palabras)
        numero_en_palabras = num2words(int(numero_), lang='es')

        return numero_en_palabras

    def toJSON(self):
        item = model_to_dict(self)
        item['numero'] = self.numero
        item['limite'] = self.limite
        item['numero'] = self.numero
        item['imagen'] = self.get_image()
        # Agregamos la conversión a palabras aquí
        item['numero_en_palabras'] = self.numero_a_palabra()

        return item

    class Meta:
        db_table = 'numeros'

        """
            	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 
            """


class VtasSorteo(models.Model):
    id = models.AutoField(primary_key=True)
    id_sorteo = models.ForeignKey(
        Sorteos, on_delete=models.CASCADE)
    fecha_sorteo = models.DateField(
        default=datetime.now, verbose_name='Fecha de Sorteo')
    totalventa = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    totalqty = models.DecimalField(max_digits=10, decimal_places=2)
    monto_premio1 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    monto_premio2 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    monto_premio3 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    id_vendedor = models.ForeignKey(
        Vendedor, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(
        Clientes, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_sorteo_premio = models.IntegerField(null=True)
    descripcion = models.TextField(null=True)
    # Campo para fecha de venta automática
    fecha_venta = models.DateTimeField(auto_now=True)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

    estado = models.CharField(
        max_length=20,
        choices=(
            ('En proceso', 'En proceso'),
            ('Facturado', 'Facturado'),
            ('Cancelado', 'Cancelado'),
            # Agrega más opciones según tus necesidades
        ),
        default='En proceso'

    )

    @classmethod
    def get_totalventas_and_totalqty(cls, id_sorteo, fecha_sorteo):
        results = cls.objects.filter(id_sorteo=id_sorteo, fecha_sorteo=fecha_sorteo).aggregate(
            totalventa=Sum('totalventa'),
            totalqty=Sum('totalqty')
        )
        return results


class VtasDetalle(models.Model):
    id = models.AutoField(primary_key=True)
    id_vtasorteo = models.ForeignKey(
        VtasSorteo, on_delete=models.CASCADE, related_name='vtasdetalles')
    fecha_sorteo = models.DateField(
        default=datetime.now, verbose_name='Fecha de Sorteo')

    id_sorteo = models.ForeignKey(
        Sorteos, on_delete=models.CASCADE)
    id_sorteo_premio = models.IntegerField(null=True)
    cantidad = models.IntegerField(default=0, null=False)
    numero = models.CharField(max_length=2, null=False)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    ganador_1 = models.BooleanField(default=False)
    ganador_2 = models.BooleanField(default=False)
    ganador_3 = models.BooleanField(default=False)
    clientes = models.ManyToManyField(Clientes, related_name='compras')

    @classmethod
    def get_stats_by_id_sorteo_and_fecha_sorteo(cls, id_sorteo, fecha_sorteo):
        results = cls.objects.filter(id_sorteo=id_sorteo, fecha_sorteo=fecha_sorteo).aggregate(
            cantidad_vendida=Sum('cantidad'),
            total_vendido=Sum('total'),
            numeros_vendidos=Count('numero', distinct=True)
        )
        return results

    @classmethod
    def get_sales_summary(cls, id_sorteo, fecha_sorteo):
        sales_data = cls.objects.filter(
            id_sorteo=id_sorteo, fecha_sorteo=fecha_sorteo)

        summary = sales_data.values('numero').annotate(
            total_cantidad_vendida=Sum('cantidad'),
            total_monto_vendido=Sum('total')
        )

        sales_summary = []
        for item in summary:
            numero = item['numero']
            cantidad_vendida = item['total_cantidad_vendida']
            monto_vendido = item['total_monto_vendido']
            sales_summary.append(
                f"{numero}, {cantidad_vendida}, {monto_vendido:.2f}")

        return sales_summary

    @classmethod
    def count_sales_items(cls, id_sorteo, fecha_sorteo):
        sales_count = cls.objects.filter(
            id_sorteo=id_sorteo, fecha_sorteo=fecha_sorteo).values('id_sorteo', 'fecha_sorteo').annotate(
            total_items=Count('numero', distinct=True)
        ).order_by('id_sorteo', 'fecha_sorteo').first()

        if sales_count:
            return sales_count['total_items']
        else:
            return 0

    @classmethod
    def get_clientes_y_tickets_de_compra(cls, numero, id_sorteo, fecha_sorteo):
        ventas = cls.objects.filter(
            numero=numero, id_sorteo=id_sorteo, fecha_sorteo=fecha_sorteo)
        clientes_tickets = []

        for venta in ventas:
            clientes_tickets.append({
                'cliente': {
                    'nombre': venta.id_vtasorteo.id_cliente.get_full_name(),
                    'cedula': venta.id_vtasorteo.id_cliente.cedula,
                    'direccion': venta.id_vtasorteo.id_cliente.direccion,
                    'email': venta.id_vtasorteo.id_cliente.email,
                    'telefono': venta.id_vtasorteo.id_cliente.telefono,
                },
                'ticket_de_compra': {
                    'id': venta.id_vtasorteo.id,
                    'fecha_sorteo': venta.id_vtasorteo.fecha_sorteo,
                    'descripcion': venta.id_vtasorteo.descripcion,
                    'pdf_file': venta.id_vtasorteo.pdf_file.url if venta.id_vtasorteo.pdf_file else None,
                    'estado': venta.id_vtasorteo.estado,
                }
            })

        return clientes_tickets


class Secuencia(models.Model):
    numero_consecutivo = models.PositiveBigIntegerField(default=1)

    def incrementar_consecutivo(self):
        self.numero_consecutivo += 1
        self.save()

    def __str__(self):
        return f'LOTTOLUCKID: {self.numero_consecutivo}'
