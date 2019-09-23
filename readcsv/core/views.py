'''
views.py
'''
import csv
import logging
import os
import time
from threading import Thread

import tweepy
from tweepy import TweepError
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render

from readcsv.core.models import AppleStore

LOG = logging.getLogger(settings.LOGGING_APPNAME)


def home(request):
    '''
    home view
    :param request:
    :return:
    '''
    if request.method == 'POST' and request.FILES['file_csv']:
        file_csv = request.FILES['file_csv']
        f_s = FileSystemStorage()
        filename = f_s.save(file_csv.name, file_csv)
        uploaded_file_url = os.path.join(settings.MEDIA_ROOT, filename)
        process = ImportFile(uploaded_file_url)
        process.start()
        return render(request, 'index.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'index.html')


def news_app(request):
    '''
    news app view
    :param request:
    :return: JsonResponse
    '''
    if not request.is_ajax():
        raise Http404

    result = \
        AppleStore.objects.filter(prime_genre='News').order_by('-rating_count_tot')
    result = result.values('id_csv', 'track_name', 'n_citacoes', 'size_bytes', 'price',
                           'prime_genre', 'rating_count_tot')
    if result:
        result = result[0]
    else:
        result = {}

    return JsonResponse(result, encoder=DjangoJSONEncoder)


def music_book_app(request):
    '''
    music book views
    :param request:
    :return: JsonResponse
    '''
    if not request.is_ajax():
        raise Http404
    result = \
        AppleStore.objects.filter(Q(prime_genre='Music') | Q(prime_genre='Book')). \
            order_by('-rating_count_tot')
    result = result.values('id_csv', 'track_name', 'n_citacoes', 'size_bytes', 'price',
                           'prime_genre', 'rating_count_tot')

    if result:
        result = result[:10]
    else:
        result = []

    return JsonResponse([r for r in result], encoder=DjangoJSONEncoder, safe=False)


def music_book_twitter_app(request):
    '''
    mucis book twitter view
    :param request:
    :return: JsonResponse
    '''
    if not request.is_ajax():
        raise Http404

    result = \
        AppleStore.objects.filter(Q(prime_genre='Music') | Q(prime_genre='Book')). \
            order_by('-n_citacoes')
    result = result.values('id_csv', 'track_name', 'n_citacoes', 'size_bytes', 'price',
                           'prime_genre', 'rating_count_tot')
    if result:
        result = result[:10]
    else:
        result = []

    return JsonResponse([r for r in result], encoder=DjangoJSONEncoder, safe=False)


def get_twitter():
    '''
    twitter view
    :return: twitter object
    '''
    auth = tweepy.OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_SECRET_KEY)
    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
    twitter = tweepy.API(auth)

    try:
        twitter.auth.get_username()
    except TweepError as e_t:
        LOG.debug('Erro twitter %s', e_t)
        raise
    return twitter


class ImportFile(Thread):
    '''
    Import file
    '''

    def __init__(self, file_name):
        Thread.__init__(self)
        self.file_name = file_name
        LOG.debug('Inicio: ImportFile %s', self.file_name)

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

        LOG.debug('Consultando twitter')
        result_apps = AppleStore.objects.filter(Q(prime_genre='Music') | Q(prime_genre='Book'))
        twitter = get_twitter()
        i = 1
        for r_a in result_apps:
            t_s = twitter.search(q='#{0}'.format(r_a.track_name))
            r_a.n_citacoes = len(t_s)
            r_a.save()

            # rate limit twitter
            i += 1
            if i > 180:
                LOG.debug('rate limit twitter: 15min')
                time.sleep(960)
                i = 1
                LOG.debug('Consultando twitter')
        LOG.debug('Fim da consulta ao twitter.')

        LOG.debug('Fim: ImportFile')
