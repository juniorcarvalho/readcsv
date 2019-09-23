'''
test module
'''
import pytest


@pytest.mark.django_db
def test_model_apple_store(applestore):
    '''
    test model AppleStore
    :param applestore:
    :return:
    '''
    assert str(applestore) == '123 - Test'
