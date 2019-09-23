'''
test module
'''
import json

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_view_get(client, applestore_2):
    '''
    test get in view music_book
    :param client:
    :param applestore_2:
    :return:
    '''
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


@pytest.mark.django_db
def test_view_get_return_empty(client):
    '''
    test return empty in get view music_book
    :param client:
    :return:
    '''
    response = client.get(reverse('music_book'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
    response_json = json.loads(response.content)
    assert response.status_code == 200
    assert response_json == []


def test_view_get_return_404(client):
    '''
    test return 404 in view music_book
    :param client:
    :return:
    '''
    response = client.get(reverse('music_book'))
    assert response.status_code == 404
