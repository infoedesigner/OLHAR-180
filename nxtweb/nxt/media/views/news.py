from django.views import generic, View
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q

from django.http import JsonResponse

from nxt.security.mixins import AdminRequiredMixin

from nxt.media.forms import SearchNewsForm, MediaForm
from nxt.media.models import Media, MediaContent

from nxt.clients.models import Category, Clipping, Client
from nxt.clients.forms import ClientClippingForm

import re

class NewsListView(AdminRequiredMixin, generic.ListView):

    template_name = 'media/news_list.html'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchNewsForm(
            company=self.request.user.company, data=self.request.GET or None
        )
        return context

    def get_queryset(self):
        form = SearchNewsForm(company=self.request.user.company, data=self.request.GET or None)
        queryset = Media.objects.filter(
            source__company=self.request.user.company, source__source_type__in=['site', 'impresso']
        )
        return form.search(queryset)


class NewsCreateView(AdminRequiredMixin, generic.CreateView):

    template_name = 'media/news_form.html'
    form_class = MediaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_clipping_form'] = ClientClippingForm(company=self.request.user.company)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'clipping':
            text = form.cleaned_data['text']
            categories = Category.objects.by_clipping(self.request.user.company, text)
            initial = self.get_initial()
            initial['categories'] = categories
            form = MediaForm(company=self.request.user.company, data=self.request.POST, initial=initial)
            context = self.get_context_data(form=form)
            context['categories'] = categories
            return self.render_to_response(context=context)
        media = form.save()
        messages.success(self.request, 'Notícia criada com sucesso!')
        action = self.request.POST.get('action')
        return redirect('media:news_list')


class NewsUpdateView(AdminRequiredMixin, generic.UpdateView):

    template_name = 'media/news_form.html'
    form_class = MediaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['client_clipping_form'] = ClientClippingForm(company=self.request.user.company)
        clippings = Clipping.objects.filter(source__media=self.object)
        context['categories'] = Category.objects.filter(pk__in=clippings.values('category'))
        return context

    def get_queryset(self):
        return Media.objects.filter(
            source__company=self.request.user.company, source__source_type__in=['site', 'impresso']
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['company'] = self.request.user.company
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        media_content = self.object.contents.first()
        initial['text'] = media_content.transcription
        initial['date'] = self.object.publish_date.date()
        initial['hour'] = self.object.publish_date.time()
        initial['newspaper_crop'] = media_content.newspaper_crop
        initial['newspaper_page'] = media_content.newspaper_page
        initial['newspaper'] = media_content.newspaper
        return initial

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'clipping':
            text = form.cleaned_data['text']
            categories = Category.objects.by_clipping(self.request.user.company, text)
            initial = self.get_initial()
            initial['categories'] = categories
            form = MediaForm(company=self.request.user.company, data=self.request.POST, initial=initial)
            context = self.get_context_data(form=form)
            context['categories'] = categories
            return self.render_to_response(context=context)
        media = form.save()
        messages.success(self.request, 'Notícia atualizada com sucesso!')
        action = self.request.POST.get('action')
        return redirect('media:news_list')


class SearchCategoryView(View):
    def get(self, request, *args, **kwargs):
        keyword = request.GET.get('keyword')
        words = re.findall(r'\w+', keyword)
        
        if words:
            categories = Category.objects.all()
            matching_categories = []
            for category in categories:
                if category.name.lower() in keyword.lower():
                    matching_categories.append(category)

                else:
                    continue
            client_ids_and_categories = list(set((category.client_id, category) for category in matching_categories))

            clients_list = []
            for client_id, category in client_ids_and_categories:
                client = Client.objects.get(id=client_id)
                client_data = {
                    'id': client.id,
                    'company_name': client.company_name,
                    'category': category.name,
                    'category_id': category.id
                }
                clients_list.append(client_data)

            return JsonResponse({'clients': clients_list})
        else:
            return JsonResponse({})

search_category = SearchCategoryView.as_view()
news_list = NewsListView.as_view()
news_create = NewsCreateView.as_view()
news_update = NewsUpdateView.as_view()
