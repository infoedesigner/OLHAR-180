from django import forms
from django.db.models import Q

from nxt.core.models import State, City
from nxt.core.choices import RATING_CHOICES, MENTION_CHOICES, EVALUATION_CHOICES

from nxt.media.models import Source

from nxt.clients.models import Client, Clipping, Category


class SearchClientForm(forms.Form):

    q = forms.CharField(label='Pesquisar', required=False)

    def search(self, queryset):
        if self.is_valid():
            q = self.cleaned_data.get('q')
            if q:
                queryset = queryset.filter(
                    Q(company_name__icontains=q) | Q(cnpj_cpf__icontains=q) | \
                    Q(email__icontains=q) | Q(city__name__icontains=q) 
                    # Codigo incompleto, gerando conflito na produção, precisa ser resolvido com o modelo (models.py)
                    # | \
                    # Q(start__date__icontains=q) | Q(end__date__icontains=q)
                )
        return queryset
class ClientForm(forms.ModelForm):

    class Meta:
        model = Client
        widgets = {
            'brand': forms.widgets.FileInput,
        }
        fields = [
            'company_name',
            'slug',
            'profile',
            'cnpj_cpf',
            'email',
            'phone',
            'cell',
            'brand',
            'postal_code',
            'address',
            'number',
            'complement',
            'state',
            'city',
            'observations',
        ]


class ClientSourceContractForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['sources_contract'].queryset = self.instance.company.sources.all()
        else:
            self.fields['sources_contract'].queryset = Source.objects.none()

    class Meta:
        model = Client
        fields = [
            'sources_contract'
        ]


class ClientSourceMainForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['sources_main'].queryset = self.instance.sources_contract.all()
        else:
            self.fields['sources_main'].queryset = Source.objects.none()

    class Meta:
        model = Client
        fields = [
            'sources_main'
        ]


class ClientClippingForm(forms.Form):

    client = forms.ModelChoiceField(queryset=Client.objects.none(), label='Cliente')

    def __init__(self, company, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = company.clients.all()


class RatingClippingForm(forms.ModelForm):

    class Meta:
        model = Clipping
        fields = [
            'marketing_value',
            'has_strength',
            'has_opportunity',
            'has_weakness',
            'has_weakness',
            'rating',
            'mention',
            'approved',
            'featured',
            'subject',
        ]


class ClippingSearchForm(forms.Form):

    q = forms.CharField(label='Pesquisa por palavras', required=False)
    categories = forms.ModelMultipleChoiceField(
        label='Categorias', required=False, queryset=Category.objects.none()
    )
    source_type = forms.ChoiceField(
        label='Tipo de Veículo', required=False, choices=[('', 'Todos os tipos')] + Source.SOURCE_TYPE_CHOICES
    )
    state = forms.ModelChoiceField(label='UF', required=False, queryset=State.objects.all())
    city = forms.ModelChoiceField(label='Município', required=False, queryset=City.objects.all())
    sources = forms.ModelMultipleChoiceField(
        queryset=Source.objects.none(), label='Veículo', required=False
    )
    author = forms.CharField(label='Autor', required=False)
    evaluation = forms.ChoiceField(
        label='Avaliação', required=False, choices=[('', 'Todas')] + EVALUATION_CHOICES
    )
    mention = forms.ChoiceField(label='Menção', required=False, choices=[('', 'Todas')] + MENTION_CHOICES)
    rating = forms.ChoiceField(
        label='Classificação', required=False, choices=[('', 'Todas')] + RATING_CHOICES
    )

    start_date = forms.DateField(label='Data inicial', required=False)
    end_date = forms.DateField(label='Data final', required=False)

    def __init__(self, client, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.company = client.company
        self.fields['sources'].queryset = self.company.sources.all()
        self.fields['categories'].queryset = client.categories.all()

    def search(self, queryset):
        if self.is_valid():
            q = self.cleaned_data.get('q')
            sources = self.cleaned_data.get('sources')
            source_type = self.cleaned_data.get('source_type')
            state = self.cleaned_data.get('state')
            city = self.cleaned_data.get('city')
            author = self.cleaned_data.get('author')
            evaluation = self.cleaned_data.get('evaluation')
            mention = self.cleaned_data.get('mention')
            rating = self.cleaned_data.get('rating')
            start_date = self.cleaned_data.get('start_date')
            end_date = self.cleaned_data.get('end_date')
            if q:
                queryset = queryset.filter(content__icontains=q)
            if sources:
                queryset = queryset.filter(source__media__source__in=sources)
            if source_type:
                queryset = queryset.filter(source__media__source__source_type=source_type)
            if state and not city:
                queryset = queryset.filter(source__media__source__state=state)
            elif city:
                queryset = queryset.filter(source__media__source__city=city)
            if author:
                queryset = queryset.filter(source__media__authors__icontains=author)
            if evaluation:
                if evaluation == 'Avaliadas':
                    queryset = queryset.filter(has_evaluation=True)
                elif evaluation == 'Não Avaliadas':
                    queryset = queryset.filter(has_evaluation=False)
                elif evaluation == 'Destaques':
                    queryset = queryset.filter(featured=True)
                elif evaluation == 'Não Aprovadas':
                    queryset = queryset.filter(approved=False)
            if mention:
                queryset = queryset.filter(mention=mention)
            if rating:
                queryset = queryset.filter(rating=rating)
            if start_date:
                queryset = queryset.filter(publish_date__gte=start_date)
            if end_date:
                queryset = queryset.filter(publish_date__lte=end_date)
        return queryset
