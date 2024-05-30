class Carrito():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        
        if not cart:
            cart = self.session['session_key'] = {}
            
        self.cart = cart
        
        
    def add(self, product, quantity=1):
        product_id = str(product['id'])
        
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += quantity
            self.cart[product_id]['total_price'] = float(product['priceUSD']) * self.cart[product_id]['quantity']

        else:
            self.cart[product_id] = {
                'name' : product['name'],
                'marca': product['marca'],
                'priceUSD': product['priceUSD'],
                'code': product['code'],
                'quantity': quantity,
                'total_price': float(product['priceUSD']) * quantity
            }
            
        self.session.modified = True
        
    def clear(self):
        self.session['session_key'] = {}
        self.session.modified = True
        
    def total(self):
        total = sum(item_info['total_price'] for item_info in self.cart.values())
        return total
    
    def remove_product(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            if self.cart[product_id]['quantity'] > 1:
                self.cart[product_id]['quantity'] -= 1
                self.cart[product_id]['total_price'] -= float(self.cart[product_id]['priceUSD'])
            else:
                del self.cart[product_id]
            self.session.modified = True