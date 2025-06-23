import os
import pandas as pd

from django import forms
from django.forms.models import inlineformset_factory
from django.db.models import Q

from nxt.newsletter.models import Contact, Newsletter, Schedule


class SearchContactForm(forms.Form):

    q = forms.CharField(label='Pesquisar', required=False)

    def search(self, queryset):
        if self.is_valid():
            q = self.cleaned_data.get('q')
            if q:
                queryset = queryset.filter(
                    Q(name__icontains=q) | Q(email__icontains=q)
                )
        return queryset

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = [
            'email',
            'name',
        ]


class ContactImportForm(forms.Form):

    contact_file = forms.FileField(label='Planilha do Excel (csv, xls ou xlsx)')

    def clean_contact_file(self):
        contact_file = self.cleaned_data.get('contact_file')
        if contact_file:
            _, extension = os.path.splitext(contact_file.name)
            if extension not in ['.xls', '.csv', '.xlsx']:
                raise forms.ValidationError('O arquivo deve ser no formato XLS, XLSX ou CSV')
            try:
                if extension == '.csv':
                    df = pd.read_csv(self.cleaned_data['contact_file'].file, sep=';')
                else:
                    df = pd.read_excel(self.cleaned_data['contact_file'].file)
            except:
                raise forms.ValidationError('Não foi possível abrir a planilha, favor conferir o formato!')
        return contact_file

    def save(self, client):
        _, extension = os.path.splitext(self.cleaned_data['contact_file'].name)
        if extension == '.csv':
            df = pd.read_csv(self.cleaned_data['contact_file'].file, sep=';')
        else:
            df = pd.read_excel(self.cleaned_data['contact_file'].file)
        column_name = df.columns[0]
        column_email = df.columns[1]
        for i, row in df.iterrows():
            if not Contact.objects.filter(client=client, email=row[column_email]).exists():
                Contact.objects.create(client=client, name=row[column_name], email=row[column_email])


class SearchNewsletterForm(forms.Form):

    q = forms.CharField(label='Pesquisar', required=False)

    def search(self, queryset):
        if self.is_valid():
            q = self.cleaned_data.get('q')
            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q)
                )
        return queryset


class NewsletterForm(forms.ModelForm):

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        self.fields['contacts'].queryset = self.client.contacts.all()
        self.fields['categories'].queryset = self.client.categories.all()

    class Meta:
        model = Newsletter
        fields = [
            'title',
            'categories',
            'contacts',
        ]


class NewsletterLayoutForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        widgets = {
            'segmentation': forms.RadioSelect,
            'news_layout': forms.RadioSelect,
        }
        fields = [
            'segmentation',
            'news_layout',
            'newsletter_layout',
            'document_style',
            'document_style_active',
            'general_style',
            'general_style_active',
            'header_style',
            'header_style_active',
            'footer_style',
            'footer_style_active',
            'title_style',
            'title_style_active',
            'media_style',
            'media_style_active',
            'link_style',
            'link_style_active',
            'resume_style',
            'resume_style_active',
        ]


ScheduleFormSet = inlineformset_factory(Newsletter, Schedule, fields=['day', 'time'], extra=1)
