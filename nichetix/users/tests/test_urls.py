import pytest
from django.urls import reverse, resolve

pytestmark = pytest.mark.django_db


def test_detail():
    assert reverse("users:detail") == "/users/detail/"
    assert resolve("/users/detail/").view_name == "users:detail"


def test_update():
    assert reverse("users:update") == "/users/update/"
    assert resolve("/users/update/").view_name == "users:update"
