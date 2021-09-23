from django.urls import path

from .views import (CheckoutOrderDetailView,
                    CheckoutCreateView,
                    CheckoutSuccessView,
                    CheckoutCancelView,
                    checkout_stripe_wh_view,
                    )

app_name = "checkout"
urlpatterns = [
    path("wh/", checkout_stripe_wh_view, name="webhook"),
    path("order/<slug:slug>/", CheckoutOrderDetailView.as_view(), name="order"),
    path("success/<slug:slug>", CheckoutSuccessView.as_view(), name="success"),
    path("cancel/<slug:slug>", CheckoutCancelView.as_view(), name="cancel"),
    path("", CheckoutCreateView.as_view(), name="checkout"),
]
