"""A lightweight, session-backed shopping cart.

Keeping the cart in the session (rather than a DB model) means a guest
can add items before creating an account, and it becomes theirs the
moment they sign up or log in — no separate 'merge carts' step needed.
"""

from decimal import Decimal

from products.models import ProductVariant

SESSION_KEY = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(SESSION_KEY)
        if cart is None:
            cart = self.session[SESSION_KEY] = {}
        self.cart = cart

    def add(self, variant_id, quantity=1):
        variant_id = str(variant_id)
        current_qty = self.cart.get(variant_id, 0)
        self.cart[variant_id] = current_qty + quantity
        self.save()

    def set_quantity(self, variant_id, quantity):
        variant_id = str(variant_id)
        if quantity <= 0:
            self.remove(variant_id)
        else:
            self.cart[variant_id] = quantity
            self.save()

    def remove(self, variant_id):
        variant_id = str(variant_id)
        if variant_id in self.cart:
            del self.cart[variant_id]
            self.save()

    def clear(self):
        self.session[SESSION_KEY] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        variant_ids = self.cart.keys()
        variants = ProductVariant.objects.select_related('product').filter(id__in=variant_ids)
        variants_by_id = {str(v.id): v for v in variants}
        for variant_id, quantity in self.cart.items():
            variant = variants_by_id.get(variant_id)
            if not variant:
                continue
            yield {
                'variant': variant,
                'quantity': quantity,
                'line_total': variant.price * quantity,
            }

    def __len__(self):
        return sum(self.cart.values())

    @property
    def total_price(self):
        return sum((item['line_total'] for item in self), Decimal('0.00'))
