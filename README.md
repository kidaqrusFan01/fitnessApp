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

**Admin login uses your email**, not username — the login field is labeled
"Email" since the custom User model authenticates on email.

## Mobile responsiveness
The site uses a fluid grid system that collapses from 4 → 2 → 1 columns,
and under 980px the top nav is replaced by a hamburger menu (`#menuToggle` /
`#mobileNav` in `base.html`) so every page stays fully navigable on phones.
The cart page switches from a table to stacked cards under 640px. All of
this lives in `static/css/style.css` — the breakpoints are `980px` and
`640px`.

## Admin
The admin is re-skinned to match the site's red/black brand
(`templates/admin/base_site.html` + `static/css/admin-theme.css`), by
overriding Django admin's own CSS custom properties rather than fighting
its stylesheet.

**Production static files:** WhiteNoise is wired in (`whitenoise.middleware.
WhiteNoiseMiddleware` + `STORAGES["staticfiles"]`) so admin CSS/JS and the
site's own static files are served correctly even with `DEBUG = False`,
without needing a separate nginx/S3 static-file setup. Before deploying:

```bash
python manage.py collectstatic
```

If the admin (or the site) ever looks unstyled again in a real deployment,
this is almost always the cause: `DEBUG=False` with no static file serving
configured — check that `collectstatic` has been run and that WhiteNoise
is still in `MIDDLEWARE`.

## Notes for next steps
- Checkout/payment is not wired up yet — the cart button is a placeholder.
  Add an `orders` app + a payment provider (Stripe is the common choice)
  when you're ready.
- Product/event images use `ImageField`; Pillow is already in requirements.
- The design system (colors, type, components) lives in `static/css/style.css`
  — reuse those classes/variables for any new templates so the site stays
  consistent.
