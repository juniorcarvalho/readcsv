import pytest
from readcsv.core.models import AppleStore
from decimal import Decimal


@pytest.fixture
@pytest.mark.django_db
def applestore():
    applestore = AppleStore()
    applestore.id_csv = 123
    applestore.n_citacoes = 10
    applestore.price = Decimal(10.0)
    applestore.prime_genre = 'News'
    applestore.track_name = 'Test'
    applestore.size_bytes = 1
    applestore.rating_count_tot = 10
    applestore.save()

    return applestore

@pytest.fixture
@pytest.mark.django_db
def applestore_2():
    applestore = AppleStore()
    applestore.id_csv = 1234
    applestore.n_citacoes = 10
    applestore.price = Decimal(10.0)
    applestore.prime_genre = 'Music'
    applestore.track_name = 'Test'
    applestore.size_bytes = 1
    applestore.rating_count_tot = 10
    applestore.save()

    return applestore

