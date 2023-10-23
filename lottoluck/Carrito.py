
class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        carrito = self.session.get("carrito")

        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito
        # Inicializa el contador de líneas en 1 al crear una instancia del carrito
        self.contadorlinea = 1

    def agregar(self, Numero, qty):

        id = str(Numero.id)

        if id not in self.carrito.keys():
            # Incrementa el contador de líneas solo cuando se agrega un nuevo producto
            self.contadorlinea += 1
            self.carrito[id] = {
                "producto_id": Numero.id,
                "linea": self.contadorlinea,
                "nombre": Numero.numero,
                "cantidad": qty,
                "precio": float(Numero.costo),
                # Convert Decimal to float
                "acumulado": float(Numero.costo)*qty,

            }
        else:
            self.carrito[id]["cantidad"] += qty
            self.carrito[id]["acumulado"] += float(Numero.costo)*qty

        self.guarda_carrito()

    def guarda_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, Numero):
        id = str(Numero.id)

        if id in self.carrito:
            if self.carrito[id]["cantidad"] <= 0:
                del self.carrito[id]
            self.guarda_carrito()

    def restar(self, Numero):
        id = str(Numero.id)
        if id in self.carrito.keys():
            self.carrito[id]["cantidad"] -= 1
            self.carrito[id]["acumulado"] -= float(Numero.costo)
            if self.carrito[id]["cantidad"] <= 0:
                self.eliminar(Numero)
            self.guarda_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.modified = True
