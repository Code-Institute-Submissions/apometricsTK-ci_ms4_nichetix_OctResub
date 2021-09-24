from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from django.urls import reverse

from .models import TicketType, Ticket
from .forms import TicketTypeForm
from nichetix.events.models import Event

User = get_user_model()


class TicketTypeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = TicketType
    slug_field = "slug"
    template_name = "tickets/ticket_type_detail.html"

    def test_func(self):
        obj = self.get_object()
        return obj.event.host == self.request.user


class TicketTypeCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
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


class TicketDetailView(DetailView):
    model = Ticket
    slug_field = "slug"
    template_name = "tickets/ticket_detail.html"


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    ordering = ["bought"]
    context_object_name = "ticket_list"
    template_name = "tickets/ticket_list.html"

    def get_queryset(self):
        return Ticket.objects.filter(order_item__order__user_profile=self.request.user)
