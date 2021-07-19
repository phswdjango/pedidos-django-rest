import pytest
from model_bakery import baker


@pytest.fixture
def logged_user(db, django_user_model):
    model_user = baker.make(django_user_model, first_name='Fulano')
    return model_user


@pytest.fixture
def client_with_logged_user(logged_user, client):
    client.force_login(logged_user)
    return client
