from django.contrib import admin

from .models import TicketType, Ticket


class TicketTypeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "event",
        "quota",
        "sale_start",
        "sale_end",
    )


admin.site.register(TicketType, TicketTypeAdmin)
