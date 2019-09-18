import pytest
from django.urls import reverse
import json


@pytest.mark.django_db
def test_view_get(client, applestore):
    response = client.get(reverse('news'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    response_json = json.loads(response.content)
    assert response.status_code == 200
    assert response_json == {'id_csv': 123,
                             'track_name': 'Test',
                             'n_citacoes': 10,
                             'size_bytes': 1,
                             'price': '10.00',
                             'prime_genre': 'News',
                             'rating_count_tot': 10
                             }