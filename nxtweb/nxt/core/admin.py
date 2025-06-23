from django.contrib import admin

from nxt.core.models import Bank, State, City


@admin.register(State)
class StateAdmin(admin.ModelAdmin):

    list_display = ['name', 'abbreviation', 'created', 'modified']
    search_fields = ['name', 'abbreviation']


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):

    list_display = ['name', 'code', 'created', 'modified']
    search_fields = ['name', 'code']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):

    list_display = ['name', 'state', 'created', 'modified']
    search_fields = ['name', 'state']
