import datetime as dt

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.contrib import messages

from nxt.media.models import Media

from nxt.security.mixins import AdminRequiredMixin

from nxt.clients.forms import (
    ClientForm, ClientSourceMainForm, SearchClientForm, ClientSourceContractForm,
)
from nxt.clients.models import (
    Category, Client, Keyword, NegativeWord, PositiveWord
)


class ClientListView(AdminRequiredMixin, generic.ListView):

    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchClientForm(data=self.request.GET or None)
        return context

    def get_queryset(self):
        form = SearchClientForm(data=self.request.GET or None)
        return form.search(Client.objects.filter(company=self.request.user.company))


class ClientCreateView(AdminRequiredMixin, generic.CreateView):

    form_class = ClientForm
    template_name = 'clients/client_form.html'

    def form_valid(self, form):
        client = form.save(commit=False)
        client.company = self.request.user.company
        client.created_by = self.request.user
        client.save()
        messages.success(self.request, 'Cliente adicionado com sucesso!')
        return redirect('clients:client_list')


class ClientUpdateView(AdminRequiredMixin, generic.UpdateView):

    form_class = ClientForm
    template_name = 'clients/client_form.html'

    def get_queryset(self):
        return Client.objects.filter(company=self.request.user.company)

    def get_success_url(self):
        messages.success(self.request, 'Cliente atualizado com sucesso!')
        return reverse('clients:client_list')


class ClientDetailView(AdminRequiredMixin, generic.DetailView):

    template_name = 'clients/client_detail.html'
    context_object_name = 'client'

    @property
    def clipping_total(self):
        _clipping_total = getattr(self, '_clipping_total', None)
        if _clipping_total is None:
            _clipping_total = self.object.clippings.count()
            self._clipping_total = _clipping_total
        return _clipping_total

    @property
    def clipping_gazette(self):
        gazette = self.object.clippings.filter(source__media__source__source_type='diariooficial').count()
        try:
            return int(100 * (gazette / self.clipping_total))
        except:
            return 0

    @property
    def clipping_site(self):
        site = self.object.clippings.filter(source__media__source__source_type='site').count()
        try:
            return int(100 * (site / self.clipping_total))
        except:
            return 0

    @property
    def clipping_radio(self):
        radio = self.object.clippings.filter(source__media__source__source_type='radio').count()
        try:
            return int(100 * (radio / self.clipping_total))
        except:
            return 0

    @property
    def clipping_tv(self):
        tv = self.object.clippings.filter(source__media__source__source_type='tv').count()
        try:
            return int(100 * (tv / self.clipping_total))
        except:
            return 0

    def get_queryset(self):
        return Client.objects.filter(company=self.request.user.company)


class ClientContractView(AdminRequiredMixin, generic.UpdateView):

    template_name = 'clients/client_contract.html'
    form_class = ClientSourceContractForm

    def get_queryset(self):
        return Client.objects.filter(company=self.request.user.company)

    def get_success_url(self):
        messages.success(self.request, 'Veículos atualizados com sucesso!')
        return reverse('clients:client_detail', kwargs={'pk': self.object.pk})


class ClientMainView(AdminRequiredMixin, generic.UpdateView):

    template_name = 'clients/client_main.html'
    form_class = ClientSourceMainForm

    def get_queryset(self):
        return Client.objects.filter(company=self.request.user.company)

    def get_success_url(self):
        messages.success(self.request, 'Veículos atualizados com sucesso!')
        return reverse('clients:client_detail', kwargs={'pk': self.object.pk})


class ClientAttendanceView(AdminRequiredMixin, generic.DetailView):

    template_name = 'clients/client_attendance.html'

    def get_queryset(self):
        return Client.objects.filter(company=self.request.user.company)

    def post(self, request, pk):
        client = self.get_object()
        action = self.request.POST.get('action')
        if action == 'delete_category':
            category = self.request.POST.get('category')
            category = get_object_or_404(Category, pk=category)
            category.delete()
            messages.success(request, 'Categoria removida com sucesso!')
        elif action == 'category':
            name = self.request.POST.get('name')
            if not name or Category.objects.filter(client=client, name=name).exists():
                messages.error(request, 'Nome de categoria deve ser único para o cliente')
            elif name:
                Category.objects.create(client=client, name=name)
        elif action == 'update_category':
            name = self.request.POST.get('name')
            category = self.request.POST.get('category')
            category = get_object_or_404(Category, pk=category, client=client)
            if not name or Category.objects.filter(client=client, name=name).exists():
                messages.error(request, 'Nome de categoria deve ser único para o cliente')
            elif name:
                category.name = name
                category.save()
                messages.success(self.request, 'Categoria atualizada com sucesso!')
        elif action == 'keyword':
            positives = self.request.POST.getlist('positive')
            source = self.request.POST.get('source')
            category = self.request.POST.get('category')
            negatives = self.request.POST.getlist('negative')
            id = self.request.POST.get('id')
            if positives and category and source:
                category = Category.objects.get(pk=category)
                keyword = Keyword()
                keyword.category = category
                keyword.source = source
                keyword.save()
                for positive in positives:
                    if positive.strip():
                        PositiveWord.objects.create(keyword=keyword, word=positive.strip())
                for negative in negatives:
                    if negative.strip():
                        NegativeWord.objects.create(keyword=keyword, word=negative.strip())
                messages.success(self.request, 'Termo adicionado com sucesso!')
        elif action == 'update_keyword':
            source = self.request.POST.get('source')
            positives = self.request.POST.getlist('positive')
            negatives = self.request.POST.getlist('negative')
            id = self.request.POST.get('id')
            if source and id:
                keyword = get_object_or_404(Keyword, pk=id)
                keyword.source = source
                keyword.save()
                for positive in positives:
                    PositiveWord.objects.get_or_create(keyword=keyword, word=positive)
                PositiveWord.objects.filter(keyword=keyword).exclude(word__in=positives).delete()
                for negative in negatives:
                    NegativeWord.objects.get_or_create(keyword=keyword, word=negative)
                NegativeWord.objects.filter(keyword=keyword).exclude(word__in=negatives).delete()
                messages.success(self.request, 'Termo salvo com sucesso!')
        elif action == 'delete_keyword':
            keyword = self.request.POST.get('keyword')
            if keyword:
                keyword = get_object_or_404(Keyword, pk=keyword)
                keyword.is_active = False
                keyword.save()
                messages.success(self.request, 'Termo apagado com sucesso!')
        return redirect('clients:client_attendance', pk=pk)


client_list = ClientListView.as_view()
client_create = ClientCreateView.as_view()
client_update = ClientUpdateView.as_view()
client_detail = ClientDetailView.as_view()
client_attendance = ClientAttendanceView.as_view()
client_contract = ClientContractView.as_view()
client_main = ClientMainView.as_view()
