import datetime as dt
from django.utils import timezone

from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from nxt.clients.models import Clipping



from nxt.security.mixins import ClientViewMixin, AdminRequiredMixin

from nxt.newsletter.forms import (
    ContactForm, NewsletterForm, SearchContactForm, SearchNewsletterForm, ScheduleFormSet,
    NewsletterLayoutForm, ContactImportForm
)

class ContactListView(AdminRequiredMixin, ClientViewMixin, generic.ListView):

    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchContactForm(data=self.request.GET or None)
        return context

    def get_queryset(self):
        form = SearchContactForm(data=self.request.GET or None)
        return form.search(self.client.contacts.all())


class ContactCreateView(AdminRequiredMixin, ClientViewMixin, generic.CreateView):

    form_class = ContactForm
    template_name = 'newsletter/contact_form.html'

    def form_valid(self, form):
        contact = form.save(commit=False)
        contact.client = self.client
        contact.save()
        messages.success(self.request, 'Contato criado com sucesso!')
        if 'add_other' in self.request.POST:
            return redirect('newsletter:contact_create', pk=self.client.pk)
        return redirect('newsletter:contact_list', pk=self.client.pk)


class ContactUpdateView(AdminRequiredMixin, ClientViewMixin, generic.UpdateView):

    form_class = ContactForm
    template_name = 'newsletter/contact_form.html'
    pk_url_kwarg = 'contact'

    def get_queryset(self):
        return self.client.contacts.all()

    def form_valid(self, form):
        contact = form.save()
        messages.success(self.request, 'Contato atualizado com sucesso!')
        if 'add_other' in self.request.POST:
            return redirect('newsletter:contact_create', pk=self.client.pk)
        return redirect('newsletter:contact_list', pk=self.client.pk)


class ContacImporttView(AdminRequiredMixin, ClientViewMixin, generic.FormView):

    template_name = 'newsletter/contact_import.html'
    form_class = ContactImportForm

    def form_valid(self, form):
        form.save(self.client)
        messages.success(self.request, 'Importação realizada com sucesso!')
        return redirect('newsletter:contact_list', self.client.pk)
#
#
#
#
#
class NewsletterListView(AdminRequiredMixin, ClientViewMixin, generic.ListView):

    paginate_by = 20
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchNewsletterForm(data=self.request.GET or None)
        return context

    def get_queryset(self):
        return self.client.newsletters.all()


class NewsletterCreateView(AdminRequiredMixin, ClientViewMixin, generic.CreateView):

    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ScheduleFormSet(data=self.request.POST or None)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client'] = self.client
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            newsletter = form.save(commit=False)
            newsletter.client = self.client
            newsletter.save()
            form.save_m2m()
            formset.instance = newsletter
            formset.save()
            messages.success(self.request, 'Newsletter criado com sucesso!')
            return redirect('newsletter:newsletter_list', pk=self.client.pk)
        context['form'] = form
        return self.render_to_response(context)


class NewsletterLayoutUpdateView(AdminRequiredMixin, ClientViewMixin, generic.UpdateView):

    form_class = NewsletterLayoutForm
    template_name = 'newsletter/newsletter_layout_form.html'
    pk_url_kwarg = 'newsletter'

    def get_queryset(self):
        return self.client.newsletters.all()

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Newsletter atualizada com sucesso!')
        return redirect('newsletter:newsletter_list', pk=self.client.pk)


class NewsletterUpdateView(AdminRequiredMixin, ClientViewMixin, generic.UpdateView):

    form_class = NewsletterForm
    template_name = 'newsletter/newsletter_form.html'
    pk_url_kwarg = 'newsletter'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = ScheduleFormSet(data=self.request.POST or None, instance=self.object)
        return context

    def get_queryset(self):
        return self.client.newsletters.all()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['client'] = self.client
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            form.save()
            formset.save()
            messages.success(self.request, 'Newsletter atualizada com sucesso!')
            return redirect('newsletter:newsletter_list', pk=self.client.pk)
        context['form'] = form
        return self.render_to_response(context)


class NewsletterPreviewView(AdminRequiredMixin, ClientViewMixin, generic.DetailView):
    template_name = 'newsletter/emails/newsletter.html'
    pk_url_kwarg = 'newsletter'

    def get_queryset(self):
        return self.client.newsletters.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        newsletter = self.get_object()
        context['title'] = newsletter.title
        context['categories'] = newsletter.categories.all()

            #Limit the clippings object to those created in a certain timeframe
        now = timezone.now()
        limit_date = now - dt.timedelta(days=25)# days = number of days since the present
        context['clippings'] = Clipping.objects.filter(
            client=newsletter.client, 
            newsletter_sent=False, 
            created__gte=limit_date
        )
        return context




contact_list = ContactListView.as_view()
contact_create = ContactCreateView.as_view()
contact_update = ContactUpdateView.as_view()
contact_import = ContacImporttView.as_view()
newsletter_list = NewsletterListView.as_view()
newsletter_create = NewsletterCreateView.as_view()
newsletter_update = NewsletterUpdateView.as_view()
newsletter_layout_update = NewsletterLayoutUpdateView.as_view()
newsletter_preview = NewsletterPreviewView.as_view()
