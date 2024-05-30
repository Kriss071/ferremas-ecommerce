from django.urls import path
from .views import *

urlpatterns = [
    path('', resumen_carrito, name='resumen_carrito'),
    path('agregar/<int:id_product>', agregar_carrito, name='agregar_carrito'),
    path('clear_cart/', clear_cart, name='clear_cart'),
    path('eliminar/<int:id_product>', eliminar_carrito, name='eliminar_carrito'),
]