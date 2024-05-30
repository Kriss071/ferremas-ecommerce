from .carrito import Carrito

def cart(request):
    return {'cart': Carrito(request)}