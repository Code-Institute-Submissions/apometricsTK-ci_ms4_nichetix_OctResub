import pytest
from django.test import RequestFactory
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import reverse

from nichetix.users.models import User
from nichetix.users.views import UserDetailView, UserUpdateView

pytestmark = pytest.mark.django_db


class TestUserDetailView:
    def test_get_object(self, user: User, request_factory: RequestFactory):
        view = UserDetailView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user


class TestUserUpdateView:
    """
    Compare "A wedge of django"
    https://github.com/feldroy/django-crash-starter/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/users/tests/test_views.py
    """
    def test_get_success_url(self, user: User, request_factory: RequestFactory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_success_url() == "/users/detail/"

    def test_get_object(self, user: User, request_factory: RequestFactory):
        view = UserUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object() == user

    def test_form_valid(self, user: User, request_factory: RequestFactory):
        form_data = {"company_name": "Test Inc"}
        request = request_factory.post(
            reverse("users:update"), form_data
        )
        request.user = user
        session_middleware = SessionMiddleware(request)
        session_middleware.process_request(request)
        msg_middleware = MessageMiddleware(request)
        msg_middleware.process_request(request)

        response = UserUpdateView.as_view()(request)
        user.refresh_from_db()

        assert response.status_code == 302
        assert user.company_name == form_data["company_name"]
