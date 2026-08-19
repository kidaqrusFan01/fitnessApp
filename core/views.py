from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from products.models import Category, Product


def home(request):
    context = {
        'categories': Category.objects.all()[:4],
        'featured_products': Product.objects.filter(is_active=True, is_featured=True)[:4],
        'upcoming_events': Event.objects.filter(
            is_published=True, start_datetime__gte=timezone.now()
        )[:3],
    }
    return render(request, 'core/home.html', context)
