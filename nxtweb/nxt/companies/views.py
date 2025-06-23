from django.views import generic
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse

from nxt.security.mixins import IsStaffRequiredMixin

from nxt.companies.forms import CompanyForm, SearchCompanyForm, DocumentForm, DocumentSearchForm
from nxt.companies.models import Company


class CompanyListView(IsStaffRequiredMixin, generic.ListView):

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchCompanyForm(data=self.request.GET or None)
        return context

    def get_queryset(self):
        form = SearchCompanyForm(data=self.request.GET or None)
        return form.search(self.request.user.companies.all())


class CompanyCreateView(IsStaffRequiredMixin, generic.CreateView):

    form_class = CompanyForm
    template_name = 'companies/company_form.html'

    def form_valid(self, form):
        company = form.save()
        self.request.user.companies.add(company)
        messages.success(self.request, 'Empresa adicionada com sucesso!')
        return redirect('companies:company_list')


class CompanyUpdateView(IsStaffRequiredMixin, generic.UpdateView):

    form_class = CompanyForm
    template_name = 'companies/company_form.html'

    def get_queryset(self):
        return self.request.user.companies.all()

    def get_success_url(self):
        messages.success(self.request, 'Empresa atualizada com sucesso!')
        return reverse('companies:company_list')


class DocumentListView(IsStaffRequiredMixin, generic.ListView):

    paginate_by = 20
    template_name = 'companies/document_list.html'

    @property
    def company(self):
        return get_object_or_404(
            Company, pk=self.kwargs['company'], pk__in=self.request.user.companies.values('pk')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DocumentSearchForm(data=self.request.GET or None)
        return context

    def get_queryset(self):
        form = DocumentSearchForm(data=self.request.GET or None)
        return form.search(self.company.documents.all())


class DocumentCreateView(IsStaffRequiredMixin, generic.CreateView):

    form_class = DocumentForm
    template_name = 'companies/document_form.html'

    @property
    def company(self):
        return get_object_or_404(
            Company, pk=self.kwargs['company'], pk__in=self.request.user.companies.values('pk')
        )

    def form_valid(self, form):
        document = form.save(commit=False)
        document.company = self.company
        document.save()
        messages.success(self.request, 'Documento adicionado com sucesso!')
        return redirect('companies:document_list', company=self.company.pk)


class DocumentUpdateView(IsStaffRequiredMixin, generic.UpdateView):

    form_class = DocumentForm
    template_name = 'companies/document_form.html'

    @property
    def company(self):
        return get_object_or_404(
            Company, pk=self.kwargs['company'], pk__in=self.request.user.companies.values('pk')
        )

    def get_queryset(self):
        return self.company.documents.all()

    def get_success_url(self):
        messages.success(self.request, 'Documento atualizado com sucesso!')
        return reverse('companies:document_list', kwargs={'company': self.company.pk})


company_list = CompanyListView.as_view()
company_create = CompanyCreateView.as_view()
company_update = CompanyUpdateView.as_view()
document_list = DocumentListView.as_view()
document_create = DocumentCreateView.as_view()
document_update = DocumentUpdateView.as_view()
