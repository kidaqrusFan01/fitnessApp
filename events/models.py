from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=140)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    capacity = models.PositiveIntegerField(default=20)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ['start_datetime']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:detail', args=[self.slug])

    @property
    def is_upcoming(self):
        return self.start_datetime >= timezone.now()

    @property
    def spots_left(self):
        taken = self.registrations.filter(status=Registration.Status.CONFIRMED).count()
        return max(self.capacity - taken, 0)


class Registration(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = 'confirmed', 'Confirmed'
        WAITLISTED = 'waitlisted', 'Waitlisted'
        CANCELLED = 'cancelled', 'Cancelled'

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='event_registrations')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.CONFIRMED)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'member')
        ordering = ['-registered_at']

    def __str__(self):
        return f'{self.member} → {self.event} ({self.status})'
