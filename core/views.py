from django.conf import settings
from django.shortcuts import render
import requests
from carrito.context_processors import formatPrice
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

API_PRODUCTS = 'https://ferremas-apirest.onrender.com/api/products/'

@csrf_exempt
def index(request):
    return render(request, 'index.html')

def catalogo(request):
    response = requests.get(API_PRODUCTS)

    if response.status_code == 200:
        products = response.json()
        products = formatPrice(products)
        context = {
            'products': products
        }
    else:
        context = {
            'error': 'No se pudo obtener los productos'
        }
        
    

    return render(request, 'catalogo.html', context)


API_GET_PAYMENT = 'https://ferremas-apirest.onrender.com/api/get-payment/'
@csrf_exempt
def retorno_flow(request):
    token = request.POST.get('token')    
    
    headers = {
                'Content-Type': 'application/json',
            }
    response = requests.get(API_GET_PAYMENT, json=token, headers=headers)
    
    response_data = response.json()
    
    context = {
        'commerceOrder': response_data['commerceOrder'],
        'requestDate': response_data['requestDate'],
        'subject': response_data['subject'],
        'payer': response_data['payer'],
        'amount': response_data['amount'],
        'currency': response_data['currency'],
        'media': response_data['media'],
        'status': response_data['status']
    }

    return render(request, 'retorno.html', context)
