from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self, **kwargs):
        """
        Get the user from request, get or 404 shouldn't be necessary (LoginRequired).
        """
        return User.objects.get(username=self.request.user.username)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    fields = [
        "company_name",
        "default_phone_number",
        "default_street_address1",
        "default_street_address2",
        "default_town_or_city",
        "default_county",
        "default_postcode",
        "default_country",
        ]
    # email? allauth version?
    model = User

    success_message = "Update successful."
    success_url = reverse_lazy("users:detail")

    def get_object(self, **kwargs):
        """
        Get the user from request, get or 404 shouldn't be necessary (LoginRequired).
        """
        return User.objects.get(username=self.request.user.username)


class UserApplicationView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["can_host"]
    template_name = "users/user_apply.html"

    success_message = "Application successful."
    success_url = reverse_lazy("users:detail")

    def get_object(self, **kwargs):
        """
        Get the user from request, get or 404 shouldn't be necessary (LoginRequired).
        """
        return User.objects.get(username=self.request.user.username)
