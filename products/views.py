from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def catalog(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True).select_related('category')

    audience = request.GET.get('audience')
    category_slug = request.GET.get('category')
    if audience:
        products = products.filter(category__audience=audience)
    if category_slug:
        products = products.filter(category__slug=category_slug)

    return render(request, 'products/catalog.html', {
        'categories': categories,
        'products': products,
        'active_audience': audience,
        'active_category': category_slug,
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('variants'),
        slug=slug, is_active=True,
    )
    return render(request, 'products/detail.html', {'product': product})
