# lottoluck/forms.py
from django import forms
from phonenumber_field.formfields import PhoneNumberField  # Importa PhoneNumberField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datetime import datetime

from .models import Clientes, NumeroSorteados, Sorteos, Vendedor


class ClienteEditForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_method = 'post'
    helper.add_input(Submit('submit', 'Guardar Cambios'))

    class Meta:
        model = Clientes
        fields = ['cedula', 'nombre', 'apellido', 'gender', 'direccion',
                  'tipocliente', 'email', 'telefono', 'birthdate', 'imagen']

    def __init__(self, *args, **kwargs):
        super(ClienteEditForm, self).__init__(*args, **kwargs)

        # Comprueba si estás en el modo de edición (actualización)
        if self.instance.pk:
            # Estás en modo de edición, utiliza el widget predeterminado para birthdate
            self.fields['birthdate'].widget = forms.DateInput()
        else:
            # Estás en modo de creación, utiliza el widget de fecha
            self.fields['birthdate'].widget = forms.DateInput(
                attrs={'type': 'date'})
    imagen = forms.ImageField(label='Foto', required=False)
    # Puedes agregar el campo email personalizado aquí
    email = forms.EmailField(max_length=255)


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['cedula', 'nombre', 'apellido', 'gender', 'direccion',
                  'tipocliente', 'email', 'telefono', 'birthdate', 'imagen']
        # fields='__all__'


class ConsultaClienteForm__2(forms.ModelForm):
    cliente_id = forms.IntegerField(label='ID del Cliente', required=False)


class ConsultaClienteForm(forms.Form):
    cedula_o_nombre = forms.CharField(
        label='Cliente',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )


class SorteosForm(forms.Form):
    # Establece el valor predeterminado en el ID 2
    valor_predeterminado = 2
    tiposorteo = forms.ModelChoiceField(

        queryset=Sorteos.objects.all(),
        required=True,
        empty_label="Seleccione El Tipo de Sorteo",  # Etiqueta para la opción vacía
        to_field_name="descripcion",  # Campo a utilizar como valor en el formulario
        # Personaliza la apariencia si es necesario
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=valor_predeterminado,  # Establece el valor predeterminado aquí,
        label="Tipo de Sorteo"  # Agrega la etiqueta a la elección de modelo


    )


class ClienteSeleccionForm2(forms.Form):
    opciones = forms.ChoiceField(choices=(), widget=forms.Select(
        attrs={'class': 'form-control'}), required=False)


class ClienteSeleccionForm(forms.Form):
    # Define una lista de tuplas para las opciones del cliente, donde el primer elemento es el valor y el segundo es la representación legible por humanos.
    opciones = forms.ChoiceField(choices=[(cliente.id, f'{cliente.apellido},{cliente.nombre} - {cliente.cedula}')
                                 for cliente in Clientes.objects.all()], widget=forms.Select(attrs={'class': 'form-control'}), required=False)


class fechaValidaSorteoForm2(forms.Form):
    fecha_valida = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Sorteo Valida'
    )


class fechaValidaSorteoForm(forms.Form):
    fecha_valida = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'showOn': 'both'}),
        label='Sorteo Valida'
    )


class fechaSorteoForm(forms.Form):
    fecha_valida = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'showOn': 'both'}),
        label='Sorteo Valida'
    )
    # Establece el valor predeterminado en el ID 2
    valor_predeterminado_sorteo = 1
    tiposorteo = forms.ModelChoiceField(

        queryset=Sorteos.objects.all(),
        required=True,
        empty_label="Seleccione El Tipo de Sorteo",  # Etiqueta para la opción vacía
        to_field_name="id",  # Campo a utilizar como valor en el formulario
        # Personaliza la apariencia si es necesario
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=valor_predeterminado_sorteo,  # Establece el valor predeterminado aquí,
        label="Tipo de Sorteo"  # Agrega la etiqueta a la elección de modelo

    )


class sorteo_vendedor_form(forms.Form):
    valor_predeterminado_vendedor = Vendedor.objects.get(id=1)
    vendedor = forms.ModelChoiceField(
        queryset=Vendedor.objects.all(),
        empty_label="Seleccione Vendedor",
        to_field_name="id",
        widget=forms.Select(attrs={'class': 'form-control'}),
        # Establece la instancia del vendedor como valor predeterminado
        initial=valor_predeterminado_vendedor,
        label="Vendedor"
    )
    # Establece el valor predeterminado en el ID 2
    valor_predeterminado_sorteo = 1
    tiposorteo = forms.ModelChoiceField(

        queryset=Sorteos.objects.all(),
        required=True,
        empty_label="Seleccione El Tipo de Sorteo",  # Etiqueta para la opción vacía
        to_field_name="id",  # Campo a utilizar como valor en el formulario
        # Personaliza la apariencia si es necesario
        widget=forms.Select(attrs={'class': 'form-control'}),
        initial=valor_predeterminado_sorteo,  # Establece el valor predeterminado aquí,
        label="Tipo de Sorteo"  # Agrega la etiqueta a la elección de modelo

    )


class VendedorForm(forms.Form):
    # Obtiene la instancia del vendedor predeterminado
    valor_predeterminado = Vendedor.objects.get(id=1)

    vendedor = forms.ModelChoiceField(
        queryset=Vendedor.objects.all(),
        empty_label="Seleccione Vendedor",
        to_field_name="nombre",
        widget=forms.Select(attrs={'class': 'form-control'}),
        # Establece la instancia del vendedor como valor predeterminado
        initial=valor_predeterminado,
        label="Vendedor"
    )


class NumeroSorteadosForm(forms.ModelForm):

    class Meta:
        model = NumeroSorteados
        fields = ['id_sorteo', 'fecha', 'referencia', 'I_premio',
                  'letras', 'serie', 'folio', 'II_premio', 'III_premio']
        labels = {
            'id_sorteo': 'Tipo de Sorteo',
            'fecha': 'Fecha del Sorteo',
            'referencia': 'No.Sorteo de LNB',
            'I_premio': 'Primer Premio',
            'II_premio': 'Segundo Premio',
            'III_premio': 'Tercer Premio',
            'letras': 'Letra del Primer Premio',
            'serie': 'No.Serie del Primer Premio',
            'folio': 'No. Folio del Primer Premio',
        }

        widgets = {
            'id_sorteo': forms.Select(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Vigencia del Sorteo', 'type': 'date'}),
            'referencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese No.Sorteo de LNB'}),
            'I_premio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primer Premio'}),
            'II_premio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Segundo Premio'}),
            'III_premio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tercer Premio'}),
            'letras': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'letras del Primer Premio'}),
            'serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. de serie del Primer Premio'}),
            'folio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'No. de Folio de Primer Premio'}),
        }

    def __init__(self, *args, **kwargs):
        super(NumeroSorteadosForm, self).__init__(*args, **kwargs)
        if 'instance' in kwargs:
            # Verifica si se proporciona una instancia del modelo
            instance = kwargs['instance']
            if instance.fecha:
                # Si el modelo tiene una fecha, establece ese valor como valor inicial
                self.initial['fecha'] = instance.fecha.strftime('%Y-%m-%d')
        else:
            # Si no se proporciona una instancia (nuevo registro), establece la fecha actual como valor inicial
            self.initial['fecha'] = datetime.now().strftime('%Y-%m-%d')
