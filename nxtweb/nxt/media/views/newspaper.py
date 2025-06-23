from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse

from nxt.security.mixins import AdminRequiredMixin

from nxt.media.serializers import SourceSerializer
from nxt.media.models import Newspaper, Source
from nxt.media.forms import NewspaperForm


class CheckNewspaperSourceView(AdminRequiredMixin, generic.View):

    def get(self, request):
        pk = request.GET.get('source')
        source = get_object_or_404(Source, pk=pk)
        serializer = SourceSerializer(instance=source)
        return JsonResponse(serializer.data)


class NewspaperListView(AdminRequiredMixin, generic.ListView):

    template_name = 'media/newspaper_list.html'
    paginate_by = 20

    def get_queryset(self):
        return Newspaper.objects.all()


class NewspaperCreateView(AdminRequiredMixin, generic.CreateView):

    template_name = 'media/newspaper_form.html'
    form_class = NewspaperForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs

    def form_valid(self, form):
        newspaper = form.save(commit=False)
        newspaper.company = self.request.user.company
        newspaper.save()
        messages.success(self.request, 'Impresso criado com sucesso!')
        return redirect('media:newspaper_list')


class NewspaperUpdateView(AdminRequiredMixin, generic.UpdateView):

    template_name = 'media/newspaper_form.html'
    form_class = NewspaperForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs

    def get_queryset(self):
        return self.request.user.company.newspapers.all()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Impresso atualizado com sucesso!')
        return redirect('media:newspaper_list')


newspaper_list = NewspaperListView.as_view()
newspaper_create = NewspaperCreateView.as_view()
newspaper_update = NewspaperUpdateView.as_view()
check_newspaper_source = CheckNewspaperSourceView.as_view()
