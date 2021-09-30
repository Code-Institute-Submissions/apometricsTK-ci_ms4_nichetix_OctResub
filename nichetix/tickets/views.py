from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.urls import reverse
from django.shortcuts import get_object_or_404

from .models import TicketType, Ticket
from .forms import TicketTypeForm
from nichetix.events.models import Event
from nichetix.core.utils import generate_qr

User = get_user_model()


class TicketTypeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    """
    Details to the ticket type for the host of the event
    """
    model = TicketType
    template_name = "tickets/ticket_type_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.event.host == self.request.user

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        event_slug = self.kwargs.get("event_slug")
        queryset = TicketType.objects.filter(event__slug=event_slug)
        return get_object_or_404(queryset, slug=slug)


class TicketTypeCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    """
    Create a new ticket type to an event
    """
    model = TicketType
    form_class = TicketTypeForm
    template_name = "tickets/ticket_type_create.html"
    success_message = "Ticket type created."

    def test_func(self, *args, **kwargs):
        event = Event.objects.get(slug=self.kwargs["event_slug"])
        return event.host == self.request.user

    def form_valid(self, form, *args, **kwargs):
        form.instance.event = Event.objects.get(slug=self.kwargs["event_slug"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "tickets:ticket-type-detail",
            kwargs={"slug": self.object.slug,
                    "event_slug": self.object.event.slug,
                    },
        )


class TicketTypeUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Update a ticket type as event host
    """
    model = TicketType
    form_class = TicketTypeForm
    slug_field = "slug"
    template_name = "tickets/ticket_type_form.html"
    success_message = "Update successful."

    def test_func(self, *args, **kwargs):
        event = Event.objects.get(slug=self.kwargs["event_slug"])
        return event.host == self.request.user

    def get_success_url(self):
        return reverse(
            "tickets:ticket-type-detail",
            kwargs={"slug": self.object.slug,
                    "event_slug": self.object.event.slug,
                    },
        )


class TicketTypeDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    """
    Mark a TicketType as deleted
    """
    model = TicketType
    slug_field = "slug"
    template_name = "tickets/ticket_type_delete.html"
    success_message = "Successfully deleted."
    fields = ["is_active"]

    def test_func(self, *args, **kwargs):
        event = Event.objects.get(slug=self.kwargs["event_slug"])
        return event.host == self.request.user

    def get_success_url(self):
        return reverse(
            "events:detail",
            kwargs={"slug": self.object.event.slug}
        )


class TicketDetailView(DetailView):
    """
    Ticket Detail view
    """
    model = Ticket
    slug_field = "slug"
    template_name = "tickets/ticket_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["svg"] = generate_qr(self.object.slug)
        return context


class TicketPrintView(DetailView):
    """
    Ticket Print view
    """
    model = Ticket
    slug_field = "slug"
    template_name = "tickets/ticket_print.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["svg"] = generate_qr(self.object.slug)
        return context


class TicketListView(LoginRequiredMixin, ListView):
    """
    List view for tickets bought by user
    """
    model = Ticket
    context_object_name = "ticket_list"
    template_name = "tickets/ticket_list.html"

    def get_queryset(self):
        return Ticket.objects.filter(order_item__order__user_profile=self.request.user).order_by("-bought")
