from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField


class User(AbstractUser):
    """
    User model to include additional information necessary for Nichetix;
    is_host = hosts events etc
    default stripe data
    """
    is_host = models.BooleanField("host status", default=False)  # todo: can_host
    company_name = models.CharField("name of the host company", max_length=80, null=True, blank=True)
    default_phone_number = models.CharField("default phone number for stripe", max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField("default street address1 for stripe",
                                               max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField("default street address2 for stripe",
                                               max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField("default town or city for stripe",
                                            max_length=40, null=True, blank=True)
    default_county = models.CharField("default county for stripe", max_length=80, null=True, blank=True)
    default_postcode = models.CharField("default postcode for stripe", max_length=20, null=True, blank=True)
    default_country = CountryField("default country for stripe", blank_label='Country', null=True, blank=True)
