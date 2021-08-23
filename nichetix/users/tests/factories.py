from typing import Any, Sequence

from django.contrib.auth import get_user_model
from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    """
    Compare "A wedge of django"
    https://www.feldroy.com/books/a-wedge-of-django
    is on Faker 8.10;
    https://github.com/feldroy/django-crash-starter/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/%7B%7Bcookiecutter.project_slug%7D%7D/users/tests/factories.py
    for Faker 8.12 dropped generate method - now evaluate;
    https://github.com/FactoryBoy/factory_boy/commit/824c6e01f91dcb07d16f51578300da3c99b6a336#diff-f57bbc6d43cc8512bb7a1ec249ce840ef810026b67792af1b4d2840c0b914bd8
    """

    class Meta:
        model = get_user_model()
        django_get_or_create = ["username"]

    username = Faker("user_name")
    email = Faker("email")

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={**kwargs, "locale": None})
        )
        self.set_password(password)
