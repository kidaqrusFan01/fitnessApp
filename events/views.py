from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .models import Event, Registration


def event_list(request):
    events = Event.objects.filter(is_published=True, start_datetime__gte=timezone.now())
    return render(request, 'events/list.html', {'events': events})


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    already_registered = (
        request.user.is_authenticated
        and Registration.objects.filter(event=event, member=request.user).exists()
    )
    return render(request, 'events/detail.html', {
        'event': event,
        'already_registered': already_registered,
    })


@login_required
def register(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)
    if Registration.objects.filter(event=event, member=request.user).exists():
        messages.info(request, "You're already registered for this event.")
    elif event.spots_left <= 0:
        Registration.objects.create(event=event, member=request.user, status=Registration.Status.WAITLISTED)
        messages.warning(request, "This event is full — you've been added to the waitlist.")
    else:
        Registration.objects.create(event=event, member=request.user, status=Registration.Status.CONFIRMED)
        messages.success(request, f'Reserved your spot for {event.title}.')
    return redirect('events:detail', slug=slug)
