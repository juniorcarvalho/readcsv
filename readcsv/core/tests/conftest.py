'''
pytest conftest
'''
from decimal import Decimal

import pytest

from readcsv.core.models import AppleStore


@pytest.fixture
@pytest.mark.django_db
def applestore():
    '''
    create object AppleStore

    :return: applestore object
    '''
    apple_store = AppleStore()
    apple_store.id_csv = 123
    apple_store.n_citacoes = 10
    apple_store.price = Decimal(10.0)
    apple_store.prime_genre = 'News'
    apple_store.track_name = 'Test'
    apple_store.size_bytes = 1
    apple_store.rating_count_tot = 10
    apple_store.save()

    return apple_store


@pytest.fixture
@pytest.mark.django_db
def applestore_2():
    '''
    create object AppleStore

    :return: applestore object
    '''
    apple_store = AppleStore()
    apple_store.id_csv = 1234
    apple_store.n_citacoes = 10
    apple_store.price = Decimal(10.0)
    apple_store.prime_genre = 'Music'
    apple_store.track_name = 'Test'
    apple_store.size_bytes = 1
    apple_store.rating_count_tot = 10
    apple_store.save()

    return applestore
