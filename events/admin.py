from django.contrib import admin

from .models import Event, Registration


class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_datetime', 'location', 'capacity', 'spots_left', 'is_published')
    list_filter = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    inlines = [RegistrationInline]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'member', 'status', 'registered_at')
    list_filter = ('status', 'event')
