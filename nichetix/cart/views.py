from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.generic import TemplateView

from nichetix.tickets.models import TicketType


class CartContentView(TemplateView):
    """
    View the content of the shopping cart
    """
    template_name = "cart/cart_content.html"


def cart_add_ticket_view(request, ticket_type_id):
    """
    Add tickets to the shopping cart, defined by TicketType and quantity
    Customized Boutique Ado
    """
    ticket_type = get_object_or_404(TicketType, pk=ticket_type_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = request.POST.get("redirect_url")
    cart = request.session.get("cart", {})

    # todo: test for sale_start < now < sale_end
    # todo: test for ticket_quantity < quota left

    if ticket_type_id in list(cart.keys()):
        cart[ticket_type_id] += quantity
        messages.success(request, f"Updated number of {ticket_type.name} to {cart[ticket_type_id]} tickets.")
    else:

        cart[ticket_type_id] = quantity
        messages.success(request, f"Added {cart[ticket_type_id]} of {ticket_type.name} to cart.")

    request.session["cart"] = cart

    return redirect(redirect_url)


def cart_remove_ticket_view(request, ticket_type_id):
    """
    Remove tickets from the shopping cart, defined by TicketType
    Customized Boutique Ado
    """
    ticket_type = get_object_or_404(TicketType, pk=ticket_type_id)
    redirect_url = reverse("cart:content")
    cart = request.session.get("cart", {})

    try:
        cart.pop(ticket_type_id)  # returns ticket_type for message
        messages.success(request, f"Removed {ticket_type.name} from your cart.")

        request.session["cart"] = cart
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f"Error removing ticket(s): {e}!")
        return redirect(redirect_url)


def cart_update_ticket_count_view(request, ticket_type_id):
    """
    Adjust number of ticket in the shopping cart, defined by TicketType
    Customized Boutique Ado
    """
    ticket_type = get_object_or_404(TicketType, pk=ticket_type_id)
    quantity = int(request.POST.get("quantity"))
    redirect_url = reverse("cart:content")
    cart = request.session.get("cart", {})

    if quantity > 0:
        cart[ticket_type_id] = quantity
        messages.success(request, f"Now {cart[ticket_type_id]} of {ticket_type.name} in your bag.")
    else:
        cart.pop(ticket_type_id)
        messages.success(request, f"Removed {ticket_type.name} from your cart.")

    request.session["cart"] = cart
    return redirect(redirect_url)
