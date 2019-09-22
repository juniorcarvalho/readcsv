import pytest
from django.conf import settings
from tweepy import TweepError

from readcsv.core.views import get_twitter


def test_get_twitter():
    twitter = get_twitter()
    username = twitter.auth.get_username()
    assert username


def test_get_twitter_404():
    settings.TWITTER_API_KEY = settings.TWITTER_API_KEY + '1'
    with pytest.raises(TweepError):
        get_twitter()
