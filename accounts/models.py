from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Prime Athletes member account.

    Extends Django's built-in user with the fields the ecosystem needs:
    a shopping preference (so we can default the catalog to the right
    section) and a saved size, so checkout is a single tap.
    """

    class ShopPreference(models.TextChoices):
        MEN = 'men', "Men's"
        WOMEN = 'women', "Women's"
        UNISEX = 'unisex', 'No preference'

    class SizeChoice(models.TextChoices):
        XS = 'XS', 'XS'
        S = 'S', 'S'
        M = 'M', 'M'
        L = 'L', 'L'
        XL = 'XL', 'XL'
        XXL = 'XXL', 'XXL'

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    shop_preference = models.CharField(
        max_length=10, choices=ShopPreference.choices, default=ShopPreference.UNISEX
    )
    saved_size = models.CharField(
        max_length=3, choices=SizeChoice.choices, blank=True,
        help_text='Default apparel size, applied at checkout.'
    )
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
