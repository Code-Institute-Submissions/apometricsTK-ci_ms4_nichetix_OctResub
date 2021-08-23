import pytest
from django.test import RequestFactory

from nichetix.users.models import User
from nichetix.users.tests.factories import UserFactory


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
