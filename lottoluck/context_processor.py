from .models import Secuencia


def factura_secuencia(request):
    secuenciafactura = None
    if request.user.is_authenticated:
        secuencia = Secuencia.objects.first()
        if secuencia:
            secuenciafactura = str(secuencia.numero_consecutivo)
    return {'factura_secuencia':  secuenciafactura}


def total_compra(request):
    total = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += float(value["acumulado"])
               # qty += int(value["cantidad"])
    return {'total_compra': total}


def total_qty(request):
    qty = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                qty += float(value["cantidad"])

    return {'total_qty': qty}


def total_linea(request):
    qty = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            qty = len(request.session["carrito"])

    return {'total_linea': qty}
