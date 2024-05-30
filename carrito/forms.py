from django import forms

class ConfirmarCompraForm(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=100)
    telefono = forms.CharField(label='Teléfono', max_length=20)
    calle = forms.CharField(label='Calle', max_length=100)
    numero = forms.CharField(label='Número', max_length=10)
    codigo_postal = forms.CharField(label='Código Postal', max_length=10)
    comentario = forms.CharField(label='Comentario', widget=forms.Textarea)
    correo = forms.EmailField(label='Correo Electrónico')