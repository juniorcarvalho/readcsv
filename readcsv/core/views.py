import csv
import logging
import os
import time
from threading import Thread

import tweepy
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render
from tweepy import TweepError

from readcsv.core.models import AppleStore

log = logging.getLogger(settings.LOGGING_APPNAME)


def home(request):
    if request.method == 'POST' and request.FILES['file_csv']:
        file_csv = request.FILES['file_csv']
        fs = FileSystemStorage()
        filename = fs.save(file_csv.name, file_csv)
        uploaded_file_url = os.path.join(settings.MEDIA_ROOT, filename)
        process = ImportFile(uploaded_file_url)
        process.start()
        return render(request, 'index.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'index.html')


def news_app(request):
    if not request.is_ajax():
        raise Http404

    result = \
        AppleStore.objects.filter(prime_genre='News').order_by('-rating_count_tot').values('id_csv', 'track_name',
                                                                                           'n_citacoes', 'size_bytes',
                                                                                           'price', 'prime_genre',
                                                                                           'rating_count_tot')
    if len(result) > 0:
        result = result[0]
    else:
        result = {}

    return JsonResponse(result, encoder=DjangoJSONEncoder)


def music_book_app(request):
    if not request.is_ajax():
        raise Http404
    result = \
        AppleStore.objects.filter(Q(prime_genre='Music') | Q(prime_genre='Book')).order_by('-rating_count_tot').values(
            'id_csv',
            'track_name',
            'n_citacoes',
            'size_bytes',
            'price',
            'prime_genre',
            'rating_count_tot')
    if len(result) > 0:
        result = result[:10]
    else:
        result = []

    return JsonResponse([r for r in result], encoder=DjangoJSONEncoder, safe=False)


def music_book_twitter_app(request):
    if not request.is_ajax():
        raise Http404

    result = \
        AppleStore.objects.filter(Q(prime_genre='Music') | Q(prime_genre='Book')).order_by('-n_citacoes').values(
            'id_csv',
            'track_name',
            'n_citacoes',
            'size_bytes',
            'price',
            'prime_genre',
            'rating_count_tot')
    if len(result) > 0:
        result = result[:10]
    else:
        result = []

    return JsonResponse([r for r in result], encoder=DjangoJSONEncoder, safe=False)


def get_twitter():
    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    twitter = tweepy.API(auth)

    try:
        twitter.auth.get_username()
    except TweepError as e:
        log.debug('Erro twitter {0}'.format(e))
        raise
    return twitter


class ImportFile(Thread):
    def __init__(self, file_name):
        Thread.__init__(self)
        self.file_name = file_name
        log.debug('Inicio: ImportFile {0}'.format(self.file_name))

    def run(self):
        AppleStore.objects.all().delete()
        with open(self.file_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[1] == 'id':
                    continue
                apple_store = AppleStore()
                apple_store.id_csv = row[1]
                apple_store.track_name = row[2]
                apple_store.size_bytes = row[3]
                valor = row[5]
                apple_store.price = float(valor)
                apple_store.prime_genre = row[12]
                apple_store.rating_count_tot = row[6]
                apple_store.save()
        os.remove(self.file_name)

        log.debug('Consultando twitter')
        result_apps = AppleStore.objects.filter(Q(prime_genre='Music') | Q(prime_genre='Book'))
        twitter = get_twitter()
        i = 1
        for r in result_apps:
            t = twitter.search(q='#{0}'.format(r.track_name))
            r.n_citacoes = len(t)
            r.save()

            # rate limit twitter
            i += 1
            if i > 180:
                log.debug('rate limit twitter: 15min')
                time.sleep(960)
                i = 1
                log.debug('Consultando twitter')
        log.debug('Fim da consulta ao twitter.')

        log.debug('Fim: ImportFile')
