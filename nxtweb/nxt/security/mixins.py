from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404

from nxt.clients.models import Client


class IsStaffRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_staff


class AdminRequiredMixin(UserPassesTestMixin):

    def test_func(self):
        return (
            self.request.user.is_authenticated and self.request.user.profile in ['administrador', 'funcionario']
        )


class ClientRequiredMixin(UserPassesTestMixin):

    is_client = True

    @property
    def client(self):
        _client = getattr(self, '_client', None)
        if _client is None:
            _client = get_object_or_404(Client, slug=self.kwargs['slug'])
            self._client = _client
        return _client

    def test_func(self):
        user = self.request.user
        if user.is_authenticated:
            if user.profile == 'cliente':
                return self.kwargs['slug'] == user.client.slug
            elif user.profile == 'funcionario':
                return Client.objects.filter(slug=self.kwargs['slug'], company=user.company).exists()
            else:
                return Client.objects.filter(
                    slug=self.kwargs['slug'], company__in=user.companies.all()
                ).exists()
        return False


class ClientViewMixin(object):

    @property
    def client(self):
        _client = getattr(self, '_client', None)
        if _client is None:
            self._client = get_object_or_404(
                Client.objects.filter(company=self.request.user.company), pk=self.kwargs['pk']
            )
        return self._client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client'] = self.client
        return context
