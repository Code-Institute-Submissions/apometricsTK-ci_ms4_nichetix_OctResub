from django.urls import path

from .views import (TicketTypeCreateView,
                    TicketTypeDetailView,
                    TicketTypeUpdateView,
                    TicketDetailView,
                    TicketListView,
                    TicketPrintView,
                    TicketTypeDeleteView,
                    )

app_name = "tickets"
urlpatterns = [
    path("type/<slug:event_slug>/create/", TicketTypeCreateView.as_view(),
         name="ticket-type-create"),
    path("type/<slug:event_slug>/<slug:slug>/update/", TicketTypeUpdateView.as_view(),
         name="ticket-type-update"),
    path("type/<slug:event_slug>/<slug:slug>/delete/", TicketTypeDeleteView.as_view(),
         name="ticket-type-delete"),
    path("type/<slug:event_slug>/<slug:slug>/", TicketTypeDetailView.as_view(),
         name="ticket-type-detail"),
    path("<slug:slug>/print/", TicketPrintView.as_view(),
         name="ticket-print"),
    path("<slug:slug>/", TicketDetailView.as_view(),
         name="ticket-detail"),
    path("", TicketListView.as_view(),
         name="tickets"),
]
