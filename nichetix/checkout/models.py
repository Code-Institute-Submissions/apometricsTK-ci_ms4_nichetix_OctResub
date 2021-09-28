from decimal import Decimal, ROUND_HALF_UP
import uuid

from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from autoslug import AutoSlugField


class Order(models.Model):
    """
    The model for Orders
    Order / Invoice Numbers have to be continuous, but shouldn't be guessable, therefore uuid/slugs
    """
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

    original_cart = models.TextField(null=False, blank=False, default="")
    stripe_pid = models.CharField(max_length=254, null=False, blank=False, default="")
    status_change = models.DateTimeField(auto_now=True)
    status = models.CharField("Order status", max_length=7, choices=Status.choices,
                              null=False, blank=False, default=Status.PENDING)

    def __str__(self):
        return f"Order Number {self.order_number}"

    @property
    def uuid_as_str(self):
        """
        AutoSlugField needs string to populate_from (uuid doesn't work)
        """
        return str(self.uuid)

    @property
    def status_change_date(self):
        """
        return only date from datetimefield status_change
        """
        return self.status_change.date()

    @property
    def order_items(self):
        """
        get order items of the order
        """
        return self.items.all()

    @property
    def order_sum_net(self):
        """
        get order total, net
        """
        return self.items.aggregate(models.Sum("price_net"))["price_net__sum"]

    @property
    def order_sum_tax(self):
        """
        get order tax
        """
        return self.items.aggregate(models.Sum("tax_amount"))["tax_amount__sum"]

    @property
    def order_total(self):
        """
        get order total
        """
        return self.order_sum_net + self.order_sum_tax

    def generate_tickets(self):
        """
        generate all tickets to the order
        """
        for item in self.order_items:
            item.generate_tickets()


class OrderItem(models.Model):
    """
    Order items,
    Quantity of TicketType, Separate price/tax to prevent change on TicketType Updates
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
        therefore TicketType updates after a buy doesn't affect already bought tickets
        """
        if not self.ticket_type:
            self.ticket_type = kwargs["ticket_type"]
        if not self.price_net:
            self.price_net = self.ticket_type.price_net
        if not self.tax_amount:
            self.tax_amount = self.ticket_type.tax_amount
        super().save(*args, **kwargs)

    @property
    def ticket_total(self):
        """
        calculate the total price of one ticket, based on net price and tax
        """
        return self.price_net + self.tax_amount

    @property
    def line_total(self):
        """
        calculate the total for the OrderItem / line
        """
        return self.quantity * self.ticket_total

    @property
    def event(self):
        """
        get the associated event
        """
        return self.ticket_type.event

    @property
    def event_name(self):
        """
        get the name of the associated event
        """
        return self.ticket_type.event.title

    @property
    def ticket_name(self):
        """
        get the name of the associated ticket type
        """
        return self.ticket_type.name

    @property
    def tickets(self):
        """
        get associated tickets
        """
        return self.ticket_type.tickets

    def generate_tickets(self):
        """
        test if tickets on this order-item are missing and generate them
        """
        if self.tickets.count() < self.quantity:
            missing_tickets = self.quantity - self.tickets.count()
            self.ticket_type.generate_tickets(missing_tickets, self)
