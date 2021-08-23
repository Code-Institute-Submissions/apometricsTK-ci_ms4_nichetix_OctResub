from django.urls import path

from .views import UserDetailView, UserUpdateView

app_name = "users"
urlpatterns = [
    path("update/", UserUpdateView.as_view(), name="update"),
    path("detail/", UserDetailView.as_view(), name="detail"),
]
