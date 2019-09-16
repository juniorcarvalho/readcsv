from django.contrib import admin
from .models import AppleStore

class AppleStoreAdmin(admin.ModelAdmin):
    list_display = ['id_csv', 'track_name']


admin.site.register(AppleStore, AppleStoreAdmin)

