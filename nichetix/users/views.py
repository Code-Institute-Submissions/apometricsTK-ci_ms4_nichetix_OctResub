from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import DetailView, UpdateView
from django.urls import reverse

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self):
        """
        Get the user from request
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

    def get_object(self):
        """
        Get the user from request
        """
        return User.objects.get(username=self.request.user.username)

    success_message = "Update successful."

    def get_success_url(self):
        """
        If successful Update, return to detail page
        """
        return reverse("users:detail")
