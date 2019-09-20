import csv
import logging
import os
from threading import Thread

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import render

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
        log.debug('Fim: ImportFile')
