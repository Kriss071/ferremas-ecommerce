from django.http import HttpResponse
from django.shortcuts import redirect, render

from carrito.context_processors import formatPrice
from .carrito import Carrito
import requests
from .forms import *

# Create your views here.

app_name = 'carrito'

API_PRODUCTS_FILTER_ID = 'https://ferremas-apirest.onrender.com/api/products/'
API_PEDIDOS = 'https://ferremas-apirest.onrender.com/api/pedidos/'
API_CREATE_PAYMENT = 'https://ferremas-apirest.onrender.com/api/create-payment/'

def resumen_carrito(request):   
    return render(request, 'carrito.html')


def agregar_carrito(request, id_product):
    cart = Carrito(request)
    
    response = requests.get(f'{API_PRODUCTS_FILTER_ID}{id_product}')
        
    if response.status_code == 200:
        product = response.json()
        print(product)
        product = formatPrice(product)
            
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

def confirmar_compra(request):
    cart = Carrito(request)
    
    if not cart.cart:
        return render(request, 'error.html', {'msg': 'Tu carrito está vacío. Por favor, agrega algunos productos antes de confirmar tu compra.'})
    
    if request.method == 'POST':
        form = ConfirmarCompraForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            total = cart.total()
            data['valor_total'] = total
            
            headers = {
                'Content-Type': 'application/json',
            }
            response = requests.post(API_CREATE_PAYMENT, json=data, headers=headers)
            if response.status_code == 200:
                response.data = response.json()

                url = response.data['url']
                token = response.data['token']
                payment_url = f"{url}?token={token}"

                response = requests.post(API_PEDIDOS, json=data)
        
                cart.clear() 
                return redirect(payment_url)
            return render(request, 'error.html', {'msg': 'CREO EL PEDIDO pero no entro a flow'})
    else:
        form = ConfirmarCompraForm()
        
    context = {
        'items_carrito': cart.cart.values(), 
        'form': form
    }
        
    return render(request, 'confirmar_compra.html', context)

