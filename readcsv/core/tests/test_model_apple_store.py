import pytest


@pytest.mark.django_db
def test_model_apple_store(applestore):
    assert str(applestore) == '123 - Test'
