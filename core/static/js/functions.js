function formatPrices() {
  // Obtener todos los elementos con la clase "price"
  var prices = document.getElementsByClassName('price');

  // Iterar sobre cada elemento y formatear el precio
  for (var i = 0; i < prices.length; i++) {
    var price = prices[i].innerText;

    // Reemplazar la coma con un punto, si existe
    price = price.replace(',', '.');

    // Convertir el precio a un número
    price = parseFloat(price);

    // Formatear el precio con separadores de miles y sin decimales
    price = price.toLocaleString('es-CL', { minimumFractionDigits: 0, maximumFractionDigits: 0 });

    // Agregar el símbolo de moneda y actualizar el contenido del elemento
    prices[i].innerText = '$' + price;
  }
}

// Llamar a la función cuando la página haya cargado
window.onload = formatPrices;
