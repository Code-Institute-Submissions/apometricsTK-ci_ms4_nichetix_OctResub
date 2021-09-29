from django.conf import settings
from django.db import models
from autoslug import AutoSlugField
from django_countries.fields import CountryField


class Location(models.Model):
    """
    Location where events are happening, null/blank True for Zoom Meetings etc
    """
    name = models.CharField("Name", max_length=120, )
    google_places_id = models.CharField("Google places id", max_length=255, null=True, blank=True)
    street_address1 = models.CharField("Street address1", max_length=80, null=True, blank=True)
    street_address2 = models.CharField("Street address2", max_length=80, null=True, blank=True)
    town_or_city = models.CharField("Town or city", max_length=40, null=True, blank=True)
    county = models.CharField("County", max_length=80, null=True, blank=True)
    postcode = models.CharField("Postcode", max_length=20, null=True, blank=True)
    country = CountryField("Country", blank_label="Country", null=True, blank=True)

    foreign_url = models.URLField("Location homepage", max_length=1024, null=True, blank=True, )
    phone_number = models.CharField("Phone number", max_length=20, null=True, blank=True)
    email = models.EmailField("Contact email", )

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    slug = AutoSlugField("Location URL", unique=True, populate_from="name")
    is_active = models.BooleanField("Active", default=True)

    def __str__(self):
        return str(self.name)


class Event(models.Model):
    """
    Event base model
    """
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, )
    title = models.CharField("Event Title", max_length=100, )
    slug = AutoSlugField("Event URL", unique=True, always_update=False, populate_from="title")
    description_short = models.CharField("Tweetable Description", max_length=280, )
    description_long = models.TextField("Text Description", )
    description_host = models.CharField("Host name and info", max_length=560, )
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="events")
    date_start = models.DateTimeField("Event Start", )
    date_end = models.DateTimeField("Event End", )

    foreign_url = models.URLField("Event homepage", max_length=1024, null=True, blank=True, )
    image = models.ImageField("Opener Image", null=True, blank=True)
    image_url = models.URLField("URL to Image", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField("Active", default=True)

    def __str__(self):
        return str(self.title)
