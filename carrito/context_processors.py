from .carrito import Carrito

def cart(request):
    carrito = Carrito(request)
    total = carrito.total()
    ivaTotal = total * 0.19
    neto = total * 0.81
    return {'cart': carrito, 'total': total, 'ivaTotal': ivaTotal, 'neto': neto}