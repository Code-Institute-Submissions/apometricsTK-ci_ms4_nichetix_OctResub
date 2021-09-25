import json
import stripe

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponse
from django.views.generic import DetailView, CreateView, RedirectView, ListView
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, reverse

from .models import Order, OrderItem
from .forms import OrderForm
from nichetix.tickets.models import TicketType
from nichetix.users.forms import UserChangeForm

DOMAIN = settings.ALLOWED_HOSTS[0]
stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_wh_secret = settings.STRIPE_WH_SECRET

User = get_user_model()


class CheckoutOrderDetailView(DetailView):
    """
    View for a generated order (pending, paid or abort)
    todo: printable invoice generator
    """
    model = Order
    slug_field = "slug"
    template_name = "checkout/checkout_order_detail.html"


class CheckoutOrderListView(LoginRequiredMixin, ListView):
    """
    View for all pending and paid orders of a user
    todo: refinement (status, order via events, ...?)
    """
    model = Order
    ordering = ["date"]
    context_object_name = "order_list"
    template_name = "checkout/checkout_order_list.html"

    def get_queryset(self):
        return Order.objects.filter(user_profile=self.request.user).exclude(status="abort")


class CheckoutSuccessView(RedirectView):
    """
    Redirect view for successful paid orders via stripe
    adds success message and redirects on order detail view
    """
    def get_redirect_url(self, *args, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             "Order processed successfully.")
        order = get_object_or_404(Order, slug=self.kwargs["slug"])
        return reverse("checkout:order", kwargs={"slug": order.slug})


class CheckoutCancelView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        """
        Redirect view for aborted orders via stripe
        adds error message and redirects back to checkout
        """
        messages.add_message(self.request, messages.ERROR,
                             "There was an error processing your checkout, please try again.")
        return reverse("checkout:checkout")


class CheckoutCreateView(CreateView):
    """
    Checkout View to check cart and add payment details,
    redirects to stripe payment page when form is valid
    todo: Checkout button doesn't update cart!
    """
    model = Order
    form_class = OrderForm
    slug_field = "slug"
    template_name = "checkout/checkout_create.html"
    success_url = "overwritten_on_valid"

    def get_initial(self):
        """
        populate user details form
        """
        initial = super(CheckoutCreateView, self).get_initial()
        initial = initial.copy()
        if self.request.user.is_authenticated:
            try:
                user = self.request.user
                initial["full_name"] = user.default_full_name
                initial["email"] = user.default_email
                initial["phone_number"] = user.default_phone_number
                initial["country"] = user.default_country
                initial["postcode"] = user.default_postcode
                initial["town_or_city"] = user.default_town_or_city
                initial["street_address1"] = user.default_street_address1
                initial["street_address2"] = user.default_street_address2
                initial["county"] = user.default_county

            except User.DoesNotExist:
                initial = initial

        return initial

    def form_valid(self, form):
        """
        Fetch cart from session and
        1. Generate Order after adding user profile and cart dump
        2. Add default data to user profile if wished
        3. Generate OrderItem objects with it
        4. Build stripe session with Order.order_items
        # todo: add stripe-doc url to object
        5. Redirect to stripe checkout session
        """
        cart = self.request.session.get("cart", {})

        if self.request.user.is_authenticated:
            form.instance.user_profile = self.request.user

        form.instance.original_cart = json.dumps(cart)
        super().form_valid(form)

        order = self.object

        if "save-info" in self.request.POST and self.request.user.is_authenticated:
            user = self.request.user
            invoice_data = {
                "default_phone_number": order.phone_number,
                "default_postcode": order.postcode,
                "default_town_or_city": order.town_or_city,
                "default_street_address1": order.street_address1,
                "default_street_address2": order.street_address2,
                "default_county": order.county,
                "default_country": order.country,
                "default_email": order.email,
                "default_full_name": order.full_name,
                "company_name": user.company_name,
            }
            user_form = UserChangeForm(invoice_data, instance=user)
            if user_form.is_valid():
                user_form.save()

        for key, value in cart.items():
            try:
                # todo: just own models? or short?
                # item = OrderItem.ticket_type.objects.get(id=key)
                item = TicketType.objects.get(id=key)
                order_item = OrderItem(
                    order=order,
                    ticket_type=item,
                    quantity=value,
                )
                order_item.save()

            except TicketType.DoesNotExist:
                messages.error(self.request, "There was a problem with your cart, please try again.")
                order.delete()

        DOMAIN = settings.ALLOWED_HOSTS[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY

        line_items = []
        for item in order.order_items:
            line_items.append({
                "name": item.ticket_type.name,
                "amount": int(item.ticket_total*100),  # price in cents
                "quantity": item.quantity,
                "currency": "eur",
            })

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            payment_method_types=[
                "card",
            ],
            mode="payment",
            success_url=DOMAIN + "/checkout/success/" + order.slug,
            cancel_url=DOMAIN + "/checkout/cancel/" + order.slug,
            customer_email=order.email,
            client_reference_id=order.uuid_as_str,
        )

        return redirect(checkout_session.url, code=303)


@csrf_exempt
def checkout_stripe_wh_view(request):
    """
    On stripe checkout.session.completed webhook:
    - Verify Signature
    - Identify connected order and update with pid and status
    - Generate the tickets
    Compare;
    https://stripe.com/docs/webhooks/signatures
    https://stripe.com/docs/api/events
    https://stripe.com/docs/stripe-cli (local testing)
    """
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=sig_header, secret=stripe_wh_secret
        )
    except ValueError as e:
        # Invalid payload
        print(e)
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    event_data = event.data.object
    stripe_pid = str(event_data.payment_intent)
    stripe_payment_status = str(event_data.payment_status)
    order_uuid = str(event_data.client_reference_id)

    try:
        order = Order.objects.get(uuid=order_uuid)
        order.stripe_pid = stripe_pid

        if event.type == "checkout.session.completed":
            if stripe_payment_status == "paid":
                order.status = stripe_payment_status
            order.save()
            if order.status == "paid":
                order.generate_tickets()

        elif event.type == "checkout.session.expired":
            order.status = "abort"
            order.save()

        else:
            print("Unhandled event type {}".format(event.type))
            order.save()

    except Order.DoesNotExist as e:
        print(e)

    return HttpResponse(status=200)
