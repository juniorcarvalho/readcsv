import pytest
from django.urls import reverse
import json


@pytest.mark.django_db
def test_view_get(client, applestore_2):
    response = client.get(reverse('music_book'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    response_json = json.loads(response.content)
    assert response.status_code == 200
    assert isinstance(response_json, list)
    assert response_json == [
        {'id_csv': 1234,
         'track_name': 'Test',
         'n_citacoes': 10,
         'size_bytes': 1,
         'price': '10.00',
         'prime_genre': 'Music',
         'rating_count_tot': 10
         }
    ]