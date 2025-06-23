from django.db.models import Q
from django import forms

from nxt.companies.models import Company, Document


class SearchCompanyForm(forms.Form):

    q = forms.CharField(label='Pesquisar', required=False)

    def search(self, queryset):
        if self.is_valid():
            q = self.cleaned_data.get('q')
            if q:
                queryset = queryset.filter(Q(company_name__icontains=q) | Q(brand_name__icontains=q))
        return queryset


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = [
            'company_name',
            'brand_name',
            'cnpj',
            'state_registration',
            'county_registration',
            'postal_code',
            'address',
            'number',
            'complement',
            'city',
            'state',
        ]


class DocumentSearchForm(forms.Form):

    q = forms.CharField(label='Pesquisar', required=False)

    def search(self, queryset):
        if self.is_valid():
            q = self.cleaned_data.get('q')
            if q:
                queryset = queryset.filter(Q(title__icontains=q) | Q(document_type__icontains=q))
        return queryset

class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = [
            'document_type',
            'title',
            'reference_date',
            'start_date',
            'end_date',
            'document_file',
        ]
