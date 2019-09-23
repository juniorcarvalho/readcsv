'''
admin.py
'''
from django.contrib import admin

from .models import AppleStore


class AppleStoreAdmin(admin.ModelAdmin):
    '''
    class AppleStoreAdmin
    '''
    list_display = ['id_csv', 'track_name', 'prime_genre']
    search_fields = ['track_name']


admin.site.register(AppleStore, AppleStoreAdmin)
