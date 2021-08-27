from django.urls import path

from .views import UserDetailView, UserUpdateView, UserApplicationView

app_name = "users"
urlpatterns = [
    path("update/", UserUpdateView.as_view(), name="update"),
    path("detail/", UserDetailView.as_view(), name="detail"),
    path("apply/", UserApplicationView.as_view(), name="apply_host"),
]
