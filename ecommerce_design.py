# Problem Statement: E-Commerce Order Management System
# You are tasked with designing an E-Commerce Order Management System. The system should support the following functionalities:
#
# User Management:
#
# Users can register, login, and manage their profiles.
# Product Catalog:
#
# Sellers can list products with details such as name, description, price, and stock quantity.
# Customers can browse and search for products.
# Shopping Cart:
#
# Users can add products to a shopping cart, modify quantities, and remove items.
# Users can view the total price of items in the cart.
# Order Processing:
#
# Users can place an order with the items in their cart.
# The system should create an order record, update product stock, and manage order status (e.g., pending, shipped, delivered, canceled).
# Payment and Checkout:
#
# Users can checkout using different payment methods (e.g., credit card, digital wallets).
# Payment details should be securely handled and stored.
# Order History:
#
# Users can view their past orders, including details of each order and its status.
# Non-Functional Requirements
# Security:
#
# Secure user authentication and data encryption.
# Secure handling of payment information.
# Scalability:
#
# The system should be able to handle a large number of users and orders simultaneously.
# Reliability:
#
# The system should be reliable and handle failures gracefully.
# Constraints and Considerations
# Assume that the payment gateway is an external service and you can interact with it via API calls.
# The system should be designed with a modular approach, keeping future extensions and integrations in mind.
import uuid


class BaseClass:

    def get_uuid(self):
        return uuid.uuid4()


class User(BaseClass):

    def __init__(self, name, email, password, user_type):
        self.name = name
        self.email = email
        self.password = hash(password)
        self.user_type = user_type  # seller, customer, admin
        self.user_id = self.get_uuid()
        self.orders = []

    def add_user_orders(self, order):
        self.orders.append(order)

    def check_order_history(self):
        return self.orders


class Product(BaseClass):

    def __init__(self, name, description, stock, category, product_price):
        self.name = name
        self.description = description
        self.stock = stock
        self.category = category  # electronics, clothing, furniture
        self.product_id = self.get_uuid()
        self.product_price = product_price


class Seller(BaseClass):

    def __init__(self, user_id):
        self.user_id = user_id
        self.products = []

    def add_products(self, product):
        self.products.append(product)


class Order(BaseClass):

    def __init__(self, product_id, status, payment_id, user_id):
        self.product_id = product_id
        self.status = status # placed, shipped, out for delivery, delivered
        self.payment_id = payment_id
        self.user_id = user_id
        self.oser_id = self.get_uuid()


class Payment(BaseClass):

    def __init__(self, amount, status, method):
        self.amount = amount
        self.status = status # processing, success, failure
        self.method = method  # cod, net banking, credit card, debit card
        self.payment_id = self.get_uuid()


class Cart(BaseClass):

    def __init__(self, user_id):
        self.products = []
        self.user_id = user_id
        self.total_value = 0

    def add_product_to_cart(self, product):
        self.products.append(product)
        self.total_value += product.product_price
        return self.products

    def get_total_cart_count(self):
        return len(self.products)

    def get_total_cart_value(self):
        return self.total_value

    def cart_checkout(self):
        self.products = None
        self.total_value = 0


class PlatformView:

    def __init__(self):

        self.user = {}
        self.products = {}
        self.carts = {}

    def create_user_cart(self, user_id):
        cart = Cart(user_id)
        self.carts[user_id] = cart
        return cart

    def create_user(self, name, email, password, user_type):
        user = User(name, email, password, user_type)
        self.user[user.user_id] = user
        return user

    def add_products(self, name, description, stock, category):
        product = Product(name, description, stock, category)
        self.products[product.product_id] = product
        return product

    def get_all_products(self, search_term):
        all_products = self.products
        results = []
        if search_term and len(search_term) > 2:
            for product in all_products:
                if search_term in product.name or search_term in product.description:
                    results.append(product)
            return results
        return all_products

    def get_user_cart(self, user_id):
        return self.carts.get(user_id)

    def get_product(self, product_id):
        return self.products.get(product_id)

    def place_order(self, user):
        cart = self.get_user_cart(
            user.user_id)
        cart_product = cart.products
        for product in cart_product:
            order = Order(product.product_id, 'placed', None, user.user_id)
            product = self.get_product(product.product_id)
            product.stock -= 1
            user.add_user_orders(order)

    def make_payment_for_order(self, user, payment_method):
        orders = user.orders
        cart = self.get_user_cart(
            user.user_id)
        payment = self.initiate_payment(
            cart.total_amount, 'processing', payment_method)
        for order in orders:
            order.payment_id = payment.payment_id
        cart.cart_checkout()

    def initiate_payment(self, amount, status, method):
        payment = Payment(amount, status, method)
        return payment


# Model Answer from AI
class BaseClass:

    def get_uuid(self):
        return uuid.uuid4()

class User(BaseClass):

    def __init__(self, name, email, password, user_type):
        self.name = name
        self.email = email
        self.password = hash(password)  # Replace with a proper hash function
        self.user_type = user_type  # 'seller', 'customer', 'admin'
        self.user_id = self.get_uuid()
        self.orders = []

    def add_user_orders(self, order):
        self.orders.append(order)

    def check_order_history(self):
        return self.orders

class Product(BaseClass):

    def __init__(self, name, description, stock, category, product_price):
        self.name = name
        self.description = description
        self.stock = stock
        self.category = category  # 'electronics', 'clothing', 'furniture'
        self.product_id = self.get_uuid()
        self.product_price = product_price

    def update_stock(self, quantity):
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

class Seller(BaseClass):

    def __init__(self, user_id):
        self.user_id = user_id
        self.products = []

    def add_products(self, product):
        self.products.append(product)

class Order(BaseClass):

    def __init__(self, products, status, payment_id, user_id):
        self.products = products
        self.status = status  # 'placed', 'shipped', 'delivered', 'canceled'
        self.payment_id = payment_id
        self.user_id = user_id
        self.order_id = self.get_uuid()

class Payment(BaseClass):

    def __init__(self, amount, status, method):
        self.amount = amount
        self.status = status  # 'processing', 'success', 'failure'
        self.method = method  # 'cod', 'net_banking', 'credit_card', 'debit_card'
        self.payment_id = self.get_uuid()

class Cart(BaseClass):

    def __init__(self, user_id):
        self.products = []
        self.user_id = user_id
        self.total_value = 0

    def add_product_to_cart(self, product, quantity):
        if product.update_stock(quantity):
            self.products.append((product, quantity))
            self.total_value += product.product_price * quantity
            return True
        return False

    def remove_product_from_cart(self, product):
        for p in self.products:
            if p[0].product_id == product.product_id:
                self.products.remove(p)
                self.total_value -= p[0].product_price * p[1]
                return True
        return False

    def get_total_cart_value(self):
        return self.total_value

    def checkout(self):
        if self.products:
            return True
        return False

class PlatformView:

    def __init__(self):
        self.users = {}
        self.products = {}
        self.carts = {}
        self.orders = {}

    def create_user(self, name, email, password, user_type):
        user = User(name, email, password, user_type)
        self.users[user.user_id] = user
        self.carts[user.user_id] = Cart(user.user_id)
        return user

    def add_product(self, name, description, stock, category, product_price):
        product = Product(name, description, stock, category, product_price)
        self.products[product.product_id] = product
        return product

    def get_all_products(self, search_term=None):
        if search_term:
            return [p for p in self.products.values() if search_term.lower() in p.name.lower() or search_term.lower() in p.description.lower()]
        return list(self.products.values())

    def get_user_cart(self, user_id):
        return self.carts.get(user_id)

    def place_order(self, user):
        cart = self.get_user_cart(user.user_id)
        if cart.checkout():
            order = Order(cart.products, 'placed', None, user.user_id)
            self.orders[order.order_id] = order
            user.add_user_orders(order)
            return order
        return None

    def make_payment(self, user, payment_method):
        order = user.orders[-1]  # Assuming last order is the one to pay
        if order.status == 'placed':
            payment = Payment(order.get_total_cart_value(), 'processing', payment_method)
            order.payment_id = payment.payment_id
            order.status = 'paid'
            return payment
        return None
