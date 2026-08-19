from django.shortcuts import get_object_or_404, redirect, render

from products.models import ProductVariant

from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_add(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    quantity = int(request.POST.get('quantity', 1))
    Cart(request).add(variant.id, quantity)
    return redirect('cart:detail')


def cart_update(request, variant_id):
    quantity = int(request.POST.get('quantity', 1))
    Cart(request).set_quantity(variant_id, quantity)
    return redirect('cart:detail')


def cart_remove(request, variant_id):
    Cart(request).remove(variant_id)
    return redirect('cart:detail')
