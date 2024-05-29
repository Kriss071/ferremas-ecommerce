from django.shortcuts import render
import requests
# Create your views here.

API_PRODUCTS = 'https://ferremas-apirest.onrender.com/api/products/'

def index(request):
    return render(request, 'index.html')

def catalogo(request):
    response = requests.get(API_PRODUCTS)

    if response.status_code == 200:
        products = response.json()
        
        context = {
            'products': products
        }
    else:
        context = {
            'error': 'No se pudo obtener los productos'
        }
        
    return render(request, 'catalogo.html', context)