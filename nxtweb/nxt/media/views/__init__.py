from django.views import generic
from django.contrib import messages
from django.urls import reverse
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404

from nxt.security.mixins import AdminRequiredMixin

from nxt.media.forms import SearchSourceForm, SourceForm


class SourceListView(AdminRequiredMixin, generic.ListView):

    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchSourceForm(data=self.request.GET or None)
        return context

    def get_queryset(self):
        form = SearchSourceForm(data=self.request.GET or None)
        return form.search(self.request.user.company.sources.all())


class SourceCreateView(AdminRequiredMixin, generic.CreateView):

    template_name = 'media/source_form.html'
    form_class = SourceForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs

    def form_valid(self, form):
        source = form.save(commit=False)
        source.company = self.request.user.company
        source.save()
        messages.success(self.request, 'Veículo adicionado com sucesso!')
        return redirect('media:source_list')


class SourceUpdateView(AdminRequiredMixin, generic.UpdateView):

    template_name = 'media/source_form.html'
    form_class = SourceForm

    def get_queryset(self):
        return self.request.user.company.sources.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs

    def form_valid(self, form):
        source = form.save()
        messages.success(self.request, 'Veículo atualizado com sucesso!')
        return redirect('media:source_list')


class SourceActiveView(AdminRequiredMixin, generic.View):

    def post(self, request, pk):
        source = get_object_or_404(self.request.user.company.sources.all(), pk=pk)
        source.is_active = True
        source.save()
        return JsonResponse({
            'success': True,
            'url': reverse('media:source_deactivate', kwargs={'pk': pk}),
        })


class SourceDeactiveView(AdminRequiredMixin, generic.View):

    def post(self, request, pk):
        source = get_object_or_404(self.request.user.company.sources.all(), pk=pk)
        source.is_active = False
        source.save()
        return JsonResponse({
            'success': True,
            'url': reverse('media:source_activate', kwargs={'pk': pk}),
        })


source_list = SourceListView.as_view()
source_create = SourceCreateView.as_view()
source_update = SourceUpdateView.as_view()
source_activate = SourceActiveView.as_view()
source_deactivate = SourceDeactiveView.as_view()
