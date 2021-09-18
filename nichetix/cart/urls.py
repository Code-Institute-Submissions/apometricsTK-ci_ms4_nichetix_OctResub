from django.urls import path

from .views import (CartContentView,
                    cart_add_ticket_view,
                    cart_remove_ticket_view,
                    cart_update_ticket_count_view,
                    )

app_name = "cart"
urlpatterns = [
    path("add/<str:ticket_type_id>/", cart_add_ticket_view, name="add"),
    path("update/<str:ticket_type_id>/", cart_update_ticket_count_view, name="update"),
    path("remove/<str:ticket_type_id>/", cart_remove_ticket_view, name="remove"),
    path("", CartContentView.as_view(), name="content"),
]
