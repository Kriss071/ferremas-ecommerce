import requests
from .carrito import Carrito

def cart(request):
    carrito = Carrito(request)
    total = carrito.total()
    ivaTotal = total * 0.19
    neto = total * 0.81
    return {'cart': carrito, 'total': total, 'ivaTotal': ivaTotal, 'neto': neto}


API_MI_INDICADOR = 'https://mindicador.cl/api/dolar'
def formatPrice(products):
    response = requests.get(API_MI_INDICADOR);
    if response.status_code == 200:
        valores = response.json()
        valorActual = valores['serie'][0]['valor']
        if isinstance(products, list):  # Verificar si hay más de un producto
            for p in products:
                p['priceUSD'] = int(float(p['priceUSD']) * valorActual)
        elif isinstance(products, dict):  # Verificar si solo hay un producto
            products['priceUSD'] = int(float(products['priceUSD']) * valorActual)
        return products
        