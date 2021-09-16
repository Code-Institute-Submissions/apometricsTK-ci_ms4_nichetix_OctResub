from django import forms

from .models import TicketType


class TicketTypeForm(forms.ModelForm):
    class Meta:
        model = TicketType
        fields = [
            "name",
            "description_long",
            "sale_start",
            "sale_end",
            "quota",
            "price_net",
            "tax",
        ]

        widgets = {
            "sale_start": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
            "sale_end": forms.widgets.DateTimeInput(attrs={"type": "datetime-local"}),
        }
