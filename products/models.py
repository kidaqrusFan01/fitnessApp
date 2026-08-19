from django.db import models
from django.urls import reverse


class Category(models.Model):
    """A shoppable section, e.g. Men's Gear, Women's Gear, Fitness Watches."""

    class Audience(models.TextChoices):
        MEN = 'men', 'Men'
        WOMEN = 'women', 'Women'
        UNISEX = 'unisex', 'Unisex'

    name = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    audience = models.CharField(max_length=10, choices=Audience.choices, default=Audience.UNISEX)
    description = models.CharField(max_length=200, blank=True)
    is_apparel = models.BooleanField(
        default=True, help_text='Uncheck for tech/accessories that use one-size variants only.'
    )
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class Product(models.Model):
    class Kind(models.TextChoices):
        APPAREL = 'apparel', 'Apparel'
        WATCH = 'watch', 'Fitness watch'
        ACCESSORY = 'accessory', 'Accessory'

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    kind = models.CharField(max_length=10, choices=Kind.choices, default=Kind.APPAREL)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:detail', args=[self.slug])

    @property
    def in_stock(self):
        return self.variants.filter(stock_quantity__gt=0).exists()


class ProductVariant(models.Model):
    """A specific purchasable version of a product: a size/colour combo.

    Watches and accessories get a single 'One size' variant so the same
    cart and stock model works across every category.
    """

    class Size(models.TextChoices):
        ONE_SIZE = 'ONE', 'One size'
        XS = 'XS', 'XS'
        S = 'S', 'S'
        M = 'M', 'M'
        L = 'L', 'L'
        XL = 'XL', 'XL'
        XXL = 'XXL', 'XXL'

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=3, choices=Size.choices, default=Size.ONE_SIZE)
    color = models.CharField(max_length=40, blank=True)
    sku = models.CharField(max_length=40, unique=True)
    price_override = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('product', 'size', 'color')
        ordering = ['size']

    def __str__(self):
        label = self.get_size_display()
        return f'{self.product.name} — {label}' + (f' / {self.color}' if self.color else '')

    @property
    def price(self):
        return self.price_override if self.price_override is not None else self.product.base_price
