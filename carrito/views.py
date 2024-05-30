from django.http import HttpResponse
from django.shortcuts import redirect, render
from .carrito import Carrito
import requests

# Create your views here.

app_name = 'carrito'

def resumen_carrito(request):   
    return render(request, 'carrito.html')


def agregar_carrito(request, id_product):
    cart = Carrito(request)
    
    response = requests.get(f'https://ferremas-apirest.onrender.com/products/{id_product}')
        
    if response.status_code == 200:
        product = response.json()
            
        if product:
            cart.add(product)
            return redirect('carrito:resumen_carrito')

        else:
            context = {
                'status': 'El producto no se encontró en la respuesta de la API'
            }
    else:
        context = {
            'status': 'Error al obtener el producto de la API'
        }
    
    return render(request, 'carrito.html', context)

def clear_cart(request):
    cart = Carrito(request)
    cart.clear()
    return render(request, 'carrito.html')

def eliminar_carrito(request, id_product):
    cart = Carrito(request)
    cart.remove_product(id_product)
    return redirect('carrito:resumen_carrito')


def actualizar_carrito  (request):
    pass