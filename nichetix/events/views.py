from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.urls import reverse
from django.utils import timezone

from .models import Event, Location
from .forms import EventForm, LocationForm
from nichetix.tickets.models import TicketType

User = get_user_model()


class EventsUpcomingListView(ListView):
    """
    Home View - List View of upcoming events
    todo: refine filter: start from now on or end from now on
    """
    model = Event
    queryset = Event.objects.filter(date_start__gte=timezone.now())
    ordering = ["date_start"]
    template_name = "events/events_upcoming.html"


class EventsManageListView(LoginRequiredMixin, ListView):
    """
    List View of Events hosted by a User
    todo: handle empty list
    todo: check if get_queryset needs a "super" call
    """
    model = Event
    template_name = "events/events_upcoming.html"

    def get_queryset(self):
        queryset = Event.objects.filter(host=self.request.user).order_by("date_start")
        return queryset


class EventsDetailView(DetailView):
    """
    Detail View of an event, added context: the ticket_types of the event
    todo: call to TicketType necessary? maybe just via the event model?
    """
    model = Event
    slug_field = "slug"
    template_name = "events/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super(EventsDetailView, self).get_context_data(**kwargs)
        context["ticket_type_list"] = TicketType.objects.filter(event=self.object)
        return context


# todo: refactor Create & Update View to a single class?
class EventsCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Create View for an Event
    """
    model = Event
    form_class = EventForm
    template_name = "events/event_create.html"
    success_message = "Event created."

    def test_func(self):
        return self.request.user.can_host

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.host = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "events:detail",
            kwargs={"slug": self.object.slug},
        )


class EventsUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update View for an Event
    """
    model = Event
    form_class = EventForm
    slug_field = "slug"
    success_message = "Update successful."

    def test_func(self):
        obj = self.get_object()
        return obj.host == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse(
            "events:detail",
            kwargs={"slug": self.object.slug},
        )


class LocationManageListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    """
    List of Locations for Events of a User (each User has own Locations)
    """
    model = Location
    ordering = ["name"]
    template_name = "events/events_locations.html"

    def test_func(self):
        return self.request.user.can_host

    def get_queryset(self):
        queryset = Location.objects.filter(owner=self.request.user).order_by("name")
        return queryset


class LocationsDetailView(DetailView):
    """
    Detail View for a Location
    """
    model = Location
    slug_field = "slug"
    template_name = "events/event_location_detail.html"


class LocationsCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Create View for a Location linked to User
    """
    model = Location
    form_class = LocationForm
    template_name = "events/events_location_create.html"
    success_message = "Location created."

    def test_func(self):
        return self.request.user.can_host

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "events:location-detail",
            kwargs={"slug": self.object.slug},
        )


class LocationsUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update View for a Location
    """
    model = Location
    form_class = LocationForm
    slug_field = "slug"
    template_name = "events/events_location_form.html"
    success_message = "Update successful."

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user

    def get_success_url(self):
        return reverse(
            "events:location-detail",
            kwargs={"slug": self.object.slug},
        )
