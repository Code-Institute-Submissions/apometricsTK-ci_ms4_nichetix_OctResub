"""nichetix URL Configuration"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls"), name="accounts"),
    path("users/", include("nichetix.users.urls"), name="users"),
    path("tickets/", include("nichetix.tickets.urls"), name="tickets"),
    path("cart/", include("nichetix.cart.urls"), name="cart"),
    path("checkout/", include("nichetix.checkout.urls"), name="checkout"),
    path("", include("nichetix.events.urls"), name="events"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
