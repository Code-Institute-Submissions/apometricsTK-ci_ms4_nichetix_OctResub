from decimal import Decimal, ROUND_HALF_UP
import uuid

from django.db import models
from django.conf import settings
from autoslug import AutoSlugField

from nichetix.events.models import Event


class TicketType(models.Model):
    """
    Ticket Type for tickets to sell

    Choices for Tax Rates
    germany: 19% base, 7% reduced for concerts and theater, no tax for education(with constraints)
    Tax Percentages are set in settings.py
    """
    BASE = "base"
    BASE_PERCENT = settings.BASE_PERCENT
    CUT = "cut"
    CUT_PERCENT = settings.CUT_PERCENT
    ZERO = "zero"
    ZERO_PERCENT = settings.ZERO_PERCENT

    TAX_RATES = (
        (BASE, BASE_PERCENT),
        (CUT, CUT_PERCENT),
        (ZERO, ZERO_PERCENT),
    )

    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    name = models.CharField("Ticket name", max_length=100, )
    slug = AutoSlugField("Ticket type URL", unique_with="event", populate_from="name")
    description_long = models.TextField("Text Description", )

    sale_start = models.DateTimeField("Sale Start", )
    sale_end = models.DateTimeField("Sale End", )

    quota = models.PositiveSmallIntegerField("Quota", )
    price_net = models.DecimalField("Price", max_digits=6, decimal_places=2)
    tax = models.CharField("Tax rate", max_length=4, choices=TAX_RATES, blank=False, default=BASE)

    def __str__(self):
        return str(self.name)

    @property
    def tax_percent(self):
        if self.tax == self.BASE:
            return Decimal(self.BASE_PERCENT)
        elif self.tax == self.CUT:
            return Decimal(self.CUT_PERCENT)
        else:
            return Decimal(self.ZERO_PERCENT)

    @property
    def tax_amount(self):
        return (self.price_net / 100 * self.tax_percent).quantize(Decimal(".01"), rounding=ROUND_HALF_UP)

    @property
    def price(self):
        return self.price_net + self.tax_amount
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
