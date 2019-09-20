import pytest
from django.conf import settings
import os
from readcsv.core.models import AppleStore
import time


def test_view_get(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_view_template(client, applestore):
    response = client.get('/')
    response_content = str(response.content)

    assert 'index.html' in [t.name for t in response.templates]
    assert 'csrfmiddlewaretoken' in response_content
    assert '<form method="post" enctype="multipart/form-data">' in response_content
    assert '<input type="file" class="form-control-file" id="csv_file"' in response_content
    assert '<button type="submit" name="btnSubmitFile">' in response_content
    assert 'id="link_listar_1"' in response_content
    assert 'id="table_1"' in response_content
    assert 'id="table_1_json"' in response_content
    assert 'id="table_1_csv"' in response_content
    assert 'id="link_listar_2"' in response_content
    assert 'id="table_2"' in response_content
    assert 'id="table_2_json"' in response_content
    assert 'id="table_2_csv"' in response_content
    assert 'id="link_listar_3"' in response_content
    assert 'id="table_3"' in response_content
    assert 'id="table_3_json"' in response_content
    assert 'id="table_3_csv"' in response_content


@pytest.mark.django_db
def test_view_home_upload_file(client):
    file_name = os.path.join(settings.BASE_DIR, 'readcsv/core/tests/assets/AppleStoreTest.csv')
    f = open(file_name, mode='r')
    post_data = {'file_csv': f}
    response = client.post('/', data=post_data)
    time.sleep(10)

    assert response.status_code == 200

    registers = AppleStore.objects.all()
    assert len(registers) == 1

