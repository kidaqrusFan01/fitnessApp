# Prime Athletes

A Django e-commerce + events platform for a men's & women's fitness brand —
apparel, fitness watches, and gym event bookings under one connected account.

## Apps
- `core` — homepage
- `accounts` — custom User model (email login, saved size, shop preference)
- `products` — categories, products, size/color variants and stock
- `events` — gym events and registrations (with waitlisting)
- `cart` — session-based shopping cart

## Getting started

```bash
python3 -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit http://127.0.0.1:8000/ for the site and http://127.0.0.1:8000/admin/
to add categories, products, variants, and events.

## Notes for next steps
- Checkout/payment is not wired up yet — the cart button is a placeholder.
  Add an `orders` app + a payment provider (Stripe is the common choice)
  when you're ready.
- Product/event images use `ImageField`; Pillow is already in requirements.
- The design system (colors, type, components) lives in `static/css/style.css`
  — reuse those classes/variables for any new templates so the site stays
  consistent.
