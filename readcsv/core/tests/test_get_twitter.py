'''
test module
'''
import pytest
from django.conf import settings
from tweepy import TweepError

from readcsv.core.views import get_twitter


def test_get_twitter():
    '''
    test function get_twitter

    :return:
    '''
    twitter = get_twitter()
    username = twitter.auth.get_username()
    assert username


def test_get_twitter_404():
    '''
    test status 404 in get_twitter

    :return:
    '''
    settings.TWITTER_API_KEY = settings.TWITTER_API_KEY + '1'
    with pytest.raises(TweepError):
        get_twitter()
