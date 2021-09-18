from decimal import Decimal

from django.shortcuts import get_object_or_404

from nichetix.tickets.models import TicketType


def cart_contents(request):
    """
    context processor for tickets in shopping cart
    customized Boutique Ado
    """
    cart_items = []
    total = 0
    ticket_count = 0
    cart = request.session.get("cart", {})

    for type_id, quantity in cart.items():
        ticket_type = get_object_or_404(TicketType, pk=type_id)
        total += ticket_type.price * quantity
        ticket_count += quantity
        cart_items.append({
            "ticket_type_id": type_id,
            "quantity": quantity,
            "ticket_type": ticket_type,
        })

    context = {
        "cart_items": cart_items,
        "total": total,
        "ticket_count": ticket_count,
    }

    return context
