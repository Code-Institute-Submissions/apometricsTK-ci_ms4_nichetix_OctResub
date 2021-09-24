from django.urls import path

from .views import (TicketTypeCreateView,
                    TicketTypeDetailView,
                    TicketTypeUpdateView,
                    TicketDetailView,
                    )

app_name = "tickets"
urlpatterns = [
    path("type/<slug:event_slug>/create/", TicketTypeCreateView.as_view(),
         name="ticket-type-create"),
    path("type/<slug:event_slug>/<slug:slug>/update/", TicketTypeUpdateView.as_view(),
         name="ticket-type-update"),
    path("type/<slug:event_slug>/<slug:slug>/", TicketTypeDetailView.as_view(),
         name="ticket-type-detail"),
    path("<slug:slug>/", TicketDetailView.as_view(),
         name="ticket-detail"),
]
