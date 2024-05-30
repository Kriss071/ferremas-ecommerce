from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('catalogo/', catalogo, name='catalogo'),
    path('retorno_flow/', retorno_flow, name='retorno')
]