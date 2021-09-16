from django.contrib import admin

from .models import Event, Location


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "host",
        "title",
        "date_start",
        "date_end",
        "foreign_url",
    )


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "street_address1",
        "street_address2",
        "town_or_city",
        "foreign_url",
    )


admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
