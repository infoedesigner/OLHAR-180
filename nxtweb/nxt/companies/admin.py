from django.contrib import admin

from nxt.companies.models import Company


@admin.register(Company)
class CompanyAdmn(admin.ModelAdmin):

    list_display = ['company_name', 'cnpj', 'is_active', 'created', 'modified']
    search_fields = ['company_name', 'cnpj']
