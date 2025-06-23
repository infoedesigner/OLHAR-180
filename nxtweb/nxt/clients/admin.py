from django.contrib import admin

from nxt.clients.models import Client, Clipping


@admin.register(Clipping)
class ClippingAdmin(admin.ModelAdmin):

    list_display = ['keyword_used', 'source', 'client', 'created']
    search_fields = ['keyword_used', 'text']
