import uuid

from django.db import models
from autoslug import AutoSlugField

from nichetix.events.models import Event


class TicketType(models.Model):
    """
    Ticket Type for tickets to sell

    Choices for Tax Rates
    germany: 19% base, 7% reduced for concerts and theater, no tax for education
    """
    BASE = "base"
    CUT = "cut"
    ZERO = "zero"

    TAX_RATES = (
        (BASE, 19.0),
        (CUT, 7.0),
        (ZERO, 0.0),
    )

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    name = models.CharField("Ticket name", max_length=100, )
    slug = AutoSlugField("Ticket type URL", unique_with="event", populate_from="name")
    description_long = models.TextField("Text Description", )

    sale_start = models.DateTimeField("Sale Start", )
    sale_end = models.DateTimeField("Sale End", )

    quota = models.PositiveSmallIntegerField("Quota", )
    price_net = models.DecimalField("Price", max_digits=6, decimal_places=2)
    tax = models.CharField("Tax rate", max_length=4, choices=TAX_RATES)

    def __str__(self):
        return str(self.name)

    # todo: implement method to get quota of remaining tickets of this type


class Ticket(models.Model):
    """
    Unique ticket sold
    # todo: implement ticket status active, cancelled, checked_in, ...
    """
    id = models.UUIDField("Ticket id", primary_key=True, default=uuid.uuid4, editable=False)
    slug = AutoSlugField("Ticket URL", populate_from="id")
    type = models.ForeignKey(TicketType, on_delete=models.PROTECT)
    # order = models.ForeignKey(TicketType, on_delete=models.PROTECT) todo: implement order model
    bought = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.type.name)

    @property
    def event(self):
        return self.type.event
