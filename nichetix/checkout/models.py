from decimal import Decimal, ROUND_HALF_UP
import uuid

from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from autoslug import AutoSlugField


class Order(models.Model):
    class Status(models.TextChoices):
        """
        Possible additions;
        CANCELED = "cancel"
        REFUND = "refund"
        ERROR = "error"
        """
        PENDING = "pending"
        PAID = "paid"
        ABORT = "abort"

    order_number = models.AutoField(primary_key=True, editable=False)
    uuid = models.UUIDField("Order id", default=uuid.uuid4, null=False, editable=False, unique=True)
    slug = AutoSlugField("Order URL", always_update=False, null=False, unique=True,
                         editable=False, populate_from="uuid_as_str",)
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                     null=True, blank=True, related_name="orders")

    full_name = models.CharField("Full Name", max_length=50, null=False, blank=False)
    email = models.EmailField("Email", max_length=254, null=False, blank=False)

    phone_number = models.CharField("Phone number", max_length=20, null=False, blank=False)
    street_address1 = models.CharField("Street address1", max_length=80, null=False, blank=False)
    street_address2 = models.CharField("Street address2", max_length=80, null=True, blank=True)
    town_or_city = models.CharField("Town or city", max_length=40, null=False, blank=False)
    county = models.CharField("County", max_length=80, null=True, blank=True)
    postcode = models.CharField("Postcode", max_length=20, null=False, blank=False)
    country = CountryField("Country", blank_label="Country *", null=False, blank=False)

    date = models.DateTimeField(auto_now_add=True)
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    original_cart = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default="")
    status_change = models.DateTimeField(auto_now=True)
    status = models.CharField("Order status", max_length=7, choices=Status.choices,
                              null=False, blank=False, default=Status.PENDING)

    def __str__(self):
        return self.order_number

    @property
    def uuid_as_str(self):
        return str(self.uuid)

    def save(self, *args, **kwargs):
        """
        Expand save method to generate xyz on order generation (=first save)
        """
        super().save(*args, **kwargs)

    @property
    def order_items(self):
        return self.items.all()

    def generate_tickets(self):
        for item in self.order_items:
            item.generate_tickets()


class OrderItem(models.Model):
    """
    Order items,
    Quantity of TicketType, Separate price/tax for updating ticket type
    """
    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.PROTECT, related_name="items")
    ticket_type = models.ForeignKey("tickets.TicketType", null=False, blank=False,
                                    on_delete=models.PROTECT, related_name="order_lines")
    quantity = models.IntegerField("Quantity", null=False, blank=False, default=0)
    price_net = models.DecimalField("Price, net", max_digits=10, decimal_places=2,
                                    null=False, blank=False, editable=False)
    tax_amount = models.DecimalField("Tax", max_digits=10, decimal_places=2,
                                     null=False, blank=False, editable=False)

    def __str__(self):
        return f"{self.ticket_type.name}, Amount: {self.quantity}, Order: {self.order.order_number}"

    def save(self, *args, **kwargs):
        """
        Expand save method to set price net and tax amount on buy (=first save)
        """
        if not self.ticket_type:
            self.ticket_type = kwargs["ticket_type"]
        if not self.price_net:
            self.price_net = self.ticket_type.price_net
        if not self.tax_amount:
            self.tax_amount = self.ticket_type.tax_amount
        super().save(*args, **kwargs)

    @property
    def line_total(self):
        return self.quantity * (self.price_net + self.tax_amount)

    @property
    def ticket_total(self):
        return self.price_net + self.tax_amount

    @property
    def event(self):
        return self.ticket_type.event

    @property
    def event_name(self):
        return self.ticket_type.event.title

    @property
    def ticket_name(self):
        return self.ticket_type.name

    @property
    def tickets(self):
        return self.ticket_type.tickets

    def generate_tickets(self):
        if self.tickets.count() < self.quantity:
            missing_tickets = self.quantity - self.tickets.count()
            self.ticket_type.generate_tickets(missing_tickets, self)
