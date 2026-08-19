from .cart import Cart


def cart_summary(request):
    """Makes the item count available to base.html (for the nav cart icon)."""
    return {'cart_item_count': len(Cart(request))}
