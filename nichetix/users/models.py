from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    """
    User model to include additional information necessary for Nichetix;
    is_host = hosts events etc
    default stripe data
    """
    can_host = models.BooleanField("Can host events", default=False)
    company_name = models.CharField("Name of the host company", max_length=80, null=True, blank=True)
    default_phone_number = models.CharField("Phone number", max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField("Street address1",
                                               max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField("Street address2",
                                               max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField("Town or city",
                                            max_length=40, null=True, blank=True)
    default_county = models.CharField("County", max_length=80, null=True, blank=True)
    default_postcode = models.CharField("Postcode", max_length=20, null=True, blank=True)
    default_country = CountryField("Country", blank_label="Country", null=True, blank=True)

    default_full_name = models.CharField("Full Name", max_length=50, null=True, blank=True)
    default_email = models.EmailField("Email", max_length=254, null=True, blank=True)
