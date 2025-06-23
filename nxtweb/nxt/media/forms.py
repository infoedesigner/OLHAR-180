import datetime as dt

from django import forms
from django.db.models import Q
from django.utils.formats import date_format

from ckeditor.fields import RichTextFormField

from nxt.core.widgets import BooleanSelect
from nxt.core.choices import DAY_CHOICES, STATE_CHOICES, DATE_XPATH_CHOICES
from nxt.core.fields import NullSelectBooleanField
from nxt.core.models import City

from nxt.media.models import Source, Media, MediaContent, Editorial, Newspaper

from nxt.clients.models import Category, Clipping


class SearchSourceForm(forms.Form):

    name = forms.CharField(label='Nome do Veículo', required=False)
    source_type = forms.ChoiceField(
        label='Selecione o Tipo do Veículo', required=False,
        choices=[('', 'Selecione o Tipo do veículo')] + Source.SOURCE_TYPE_CHOICES,
    )
    state = forms.ChoiceField(
        label='Selecione um Estado', choices=[('', 'Selecione um Estado')] + STATE_CHOICES, required=False
    )
    priority = NullSelectBooleanField(label='Prioridade', required=False, empty_label='Selecione a Prioridade')

    def search(self, queryset):
        if self.is_valid():
            name = self.cleaned_data.get('name')
            source_type = self.cleaned_data.get('source_type')
            state = self.cleaned_data.get('state')
            priority = self.cleaned_data.get('priority')
            if name:
                queryset = queryset.filter(name__icontains=name)
            if source_type:
                queryset = queryset.filter(source_type=source_type)
            if state:
                queryset = queryset.filter(state=state)
            if priority:
                queryset = queryset.filter(priority=priority)
        return queryset


class SourceForm(forms.ModelForm):

    publish_days = forms.MultipleChoiceField(
        label='Dias de Publicação', required=False, choices=DAY_CHOICES,
        widget=forms.CheckboxSelectMultiple
    )
    marketing_value = forms.DecimalField(label='Vl publicit. padrão', localize=True, required=False)

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company = company
        now = dt.datetime.now()
        self.fields['date_format'].choices = [
            (key, date_format(now, key)) for key, value in DATE_XPATH_CHOICES
        ]

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name:
            sources = self.company.sources.filter(name__iexact=name)
            if self.instance and self.instance.pk:
                sources = sources.exclude(pk=self.instance.pk)
            if sources.exists():
                raise forms.ValidationError('Já existe um Veículo com este nome!')
        return name

    def clean_url_root(self):
        url_root = self.cleaned_data.get('url_root')
        if url_root:
            sources = self.company.sources.filter(url_root__iexact=url_root)
            if self.instance and self.instance.pk:
                sources = sources.exclude(pk=self.instance.pk)
            if sources.exists():
                raise forms.ValidationError('Já existe um Veículo com este Link!')
        return url_root

    class Meta:
        model = Source
        widgets = {
            'priority': BooleanSelect
        }
        fields = [
            'name',
            'source_type',
            'priority',
            'marketing_value',
            'state',
            'city',
            'website',
            'frequency',
            'audience',
            'publish_days',
            'url_root',
            'url_xpath',
            'date_xpath',
            'date_format',
            'title_xpath',
            'headline_xpath',
            'author_xpath',
            'text_xpath',
        ]


class SearchNewsForm(forms.Form):

    source = forms.ModelChoiceField(queryset=Source.objects.none(), label='Veículo', required=False)
    title = forms.CharField(label='Busca no título', required=False)
    text = forms.CharField(label='Busca no texto', required=False)
    media_content_type = forms.ChoiceField(
        label='Tipo da Notícia', required=False,
        choices=[('', 'TODOS OS TIPOS')] + Media.MEDIA_TYPE_CHOICES
    )
    city = forms.CharField(label='Cidade', required=False)
    state = forms.ChoiceField(
        label='Estado', required=False, choices=[('', 'TODOS OS ESTADOS')] + STATE_CHOICES
    )
    start_date = forms.DateField(label='Data Inicial', required=False)
    end_date = forms.DateField(label='Data Final', required=False)

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company = company
        self.fields['source'].queryset = self.company.sources.filter(
            source_type__in=['site', 'impresso']
        )

    def search(self, queryset):
        if self.is_valid():
            source = self.cleaned_data.get('source')
            title = self.cleaned_data.get('title')
            text = self.cleaned_data.get('text')
            media_content_type = self.cleaned_data.get('media_content_type')
            city = self.cleaned_data.get('city')
            state = self.cleaned_data.get('state')
            start_date = self.cleaned_data.get('start_date')
            end_date = self.cleaned_data.get('end_date')
            if source:
                queryset = queryset.filter(source=source)
            if title:
                queryset = queryset.filter(title__icontains=title)
            if text:
                media_content = MediaContent.objects.filter(
                    transcription__icontains=text
                ).values('media')
                queryset = queryset.filter(
                    Q(resume__icontains=text) | Q(pk__in=media_content)
                )
            if media_content_type:
                queryset = queryset.filter(media_content_type=media_content_type)
            if city:
                queryset = queryset.filter(source__city__icontains=city)
            if state:
                queryset = queryset.filter(source__state=state)
            if start_date:
                queryset = queryset.filter(publish_date__gte=start_date)
            if end_date:
                queryset = queryset.filter(publish_date__lte=end_date)
        return queryset


class MediaForm(forms.ModelForm):

    text = RichTextFormField(required=False, label='Texto da Notícia')
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), required=False)
    date = forms.DateField(label='Data da publicação')
    hour = forms.TimeField(label='Horário da publicação')
    newspaper = forms.ModelChoiceField(
        queryset=Newspaper.objects.none(), label='Selecione o Impresso', required=False
    )
    newspaper_page = forms.IntegerField(label='Número da página', min_value=1, required=False)
    newspaper_crop = forms.CharField(widget=forms.HiddenInput, required=False)

    def __init__(self, company, *args, **kwargs):
        initial = kwargs.get('initial', {})
        initial['publish_date'] = dt.datetime.now()
        super().__init__(*args, **kwargs)
        self.company = company
        self.fields['source'].queryset = self.company.sources.filter(source_type__in=['site', 'impresso'])
        self.fields['newspaper'].queryset = self.company.newspapers.all()

    def save(self):
        media = super().save(commit=False)
        date = self.cleaned_data['date']
        hour = self.cleaned_data['hour']
        media.publish_date = dt.datetime(date.year, date.month, date.day, hour.hour, hour.minute)
        media.save()
        text = self.cleaned_data['text']
        media_content = media.contents.first()
        if not media_content:
            media_content = MediaContent.objects.create(
                media=media, transcription=text, order=1, processed=True, processed_clipping=True
            )
        else:
            media_content.transcription = text
        media_content.newspaper = self.cleaned_data.get('newspaper')
        media_content.newspaper_page = self.cleaned_data.get('newspaper_page')
        media_content.newspaper_crop = self.cleaned_data.get('newspaper_crop', '')
        media_content.save()
        for category in self.cleaned_data['categories']:
            if not Clipping.objects.filter(source=media_content, client=category.client).exists():
                Clipping.objects.create(
                    keyword_used='', text=text, client=category.client, source=media_content,
                    category=category, publish_date=media.publish_date, content=media_content.transcription
                )
        return media

    class Meta:
        model = Media
        fields = [
            'title',
            'media_content_type',
            'editorial',
            'url',
            'source',
            'resume',
            'authors',
        ]


class EditorialForm(forms.ModelForm):

    def __init__(self, source, *args, **kwarg):
        super().__init__(*args, **kwarg)
        self.source = source
        now = dt.datetime.now()
        self.fields['date_format'].choices = [
            (key, date_format(now, key)) for key, value in DATE_XPATH_CHOICES
        ]

    class Meta:
        model = Editorial
        fields = [
            'name',
            'url',
            'marketing_value',
            'frequency',
            'use_configuration_source',
            'url_xpath',
            'title_xpath',
            'headline_xpath',
            'date_xpath',
            'date_format',
            'author_xpath',
            'text_xpath',
        ]


class NewspaperForm(forms.ModelForm):

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company = company
        self.fields['source'].queryset = self.company.sources.filter(source_type='impresso')

    class Meta:
        model = Newspaper
        fields = [
            'source',
            'publish_date',
            'pdf_file',
        ]
