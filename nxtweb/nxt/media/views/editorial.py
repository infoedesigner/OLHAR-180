from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404

from nxt.security.mixins import AdminRequiredMixin

from nxt.media.models import Source, Editorial
from nxt.media.forms import EditorialForm


class EditorialListView(AdminRequiredMixin, generic.ListView):

    paginate_by = 20
    template_name = 'media/editorial_list.html'

    @property
    def source(self):
        _source = getattr(self, '_source', None)
        if _source is None:
            _source = get_object_or_404(
                Source.objects.filter(company=self.request.user.company), pk=self.kwargs['pk']
            )
            self._source = _source
        return _source

    def get_queryset(self):
        return self.source.editorials.all()


class EditorialCreateView(AdminRequiredMixin, generic.CreateView):

    template_name = 'media/editorial_form.html'
    form_class = EditorialForm

    @property
    def source(self):
        _source = getattr(self, '_source', None)
        if _source is None:
            _source = get_object_or_404(
                Source.objects.filter(company=self.request.user.company), pk=self.kwargs['pk']
            )
            self._source = _source
        return _source

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['source'] = self.source
        return kwargs

    def form_valid(self, form):
        editorial = form.save(commit=False)
        editorial.source = self.source
        editorial.save()
        messages.success(self.request, 'Editoria criada com sucesso!')
        return redirect('media:editorial_list', pk=self.source.pk)


class EditorialUpdateView(AdminRequiredMixin, generic.UpdateView):

    template_name = 'media/editorial_form.html'
    form_class = EditorialForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['source'] = self.source
        return kwargs

    @property
    def source(self):
        return self.object.source

    def get_success_url(self) -> str:
        messages.success(self.request, 'Editorial atualizado com sucesso!')
        return reverse('media:editorial_list', kwargs={'pk': self.source.pk})

    def get_queryset(self):
        sources = Source.objects.filter(company=self.request.user.company)
        return Editorial.objects.filter(source__in=sources.values('pk'))


editorial_list = EditorialListView.as_view()
editorial_create = EditorialCreateView.as_view()
editorial_update = EditorialUpdateView.as_view()
