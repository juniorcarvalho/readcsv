from django.db import models

class AppleStore(models.Model):
    id_csv = models.IntegerField('ID')
    track_name = models.CharField('Track Name', max_length=255)
    n_citacoes = models.IntegerField('Nro. Citações', blank=True, null=True)
    size_bytes = models.IntegerField('Size bytes', blank=True, null=True)
    price = models.DecimalField('Price', blank=True, null=True, decimal_places=2, max_digits=10)
    prime_genre = models.CharField('Prime Genre', max_length=255)
    rating_count_tot = models.IntegerField('Rating Count Tot')

    def __str__(self):
        return '{0} - {1}'.format(self.id_csv, self.track_name)


