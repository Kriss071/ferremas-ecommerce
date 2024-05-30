from django.http import HttpResponse
from django.shortcuts import redirect, render
from .carrito import Carrito
import requests
from .forms import *

# Create your views here.

app_name = 'carrito'

API_PRODUCTS_FILTER_ID = 'http://127.0.0.1:8080/products/'
API_PEDIDOS = 'http://127.0.0.1:8080/api/pedidos/'
API_CREATE_PAYMENT = 'http://127.0.0.1:8080/api/create-payment/'

def resumen_carrito(request):   
    return render(request, 'carrito.html')


def agregar_carrito(request, id_product):
    cart = Carrito(request)
    
    response = requests.get(f'{API_PRODUCTS_FILTER_ID}{id_product}')
        
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
            
            response = requests.post(API_PEDIDOS, json=data)
            
            if response.status_code == 201:
                headers = {
                    'Content-Type': 'application/json',
                }
                response = requests.post(API_CREATE_PAYMENT, json=data, headers=headers)
                if response.status_code == 200:
                    response.data = response.json()
                    print('=== Response ===')
                    print(response)
                    print('=== ==== ===')
                    print('=== Response.data ===')
                    print(response.data)
                    print('=== ==== ===')
                    
                    cart.clear() 
                    return render(request, 'error.html', {'msg': 'CREO EL PEDIDO y entro a flow'})    
                return render(request, 'error.html', {'msg': 'CREO EL PEDIDO pero no entro a flow'})
            else: 
                return render(request, 'error.html', {'msg': 'No creo el pedido'})
    else:
        form = ConfirmarCompraForm()
        
    context = {
        'items_carrito': cart.cart.values(), 
        'form': form
    }
        
    return render(request, 'confirmar_compra.html', context)

