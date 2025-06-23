import datetime as dt
from urllib.parse import quote
from datetime import timedelta, date
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic import ListView
from nxt.security.mixins import AdminRequiredMixin, ClientRequiredMixin
from django.utils import timezone
from nxt.clients.reports import export_clippings
from nxt.clients.forms import RatingClippingForm, ClippingSearchForm
from nxt.clients.models import Clipping, Category



class ClippingListView(ClientRequiredMixin, generic.ListView):

    template_name = 'clients/clipping_list.html'
    paginate_by = 20

    @property
    def date(self):
        try:
            date = self.request.GET['date']
            return dt.datetime.strptime(date, '%Y-%m-%d')
        except:
            return None

    def get_queryset(self):
        queryset = self.client.clippings.all()
        start = self.date or dt.date.today()
        start = dt.datetime(year=start.year, month=start.month, day=start.day)
        end = dt.datetime(year=start.year, month=start.month, day=start.day) + dt.timedelta(days=1)
        queryset = queryset.filter(publish_date__gte=start, publish_date__lt=end)
        source_type = self.request.GET.get('source_type')
        if source_type:
            queryset = queryset.filter(
                source__media__source__source_type=source_type
            )
        return queryset


class ClippingSearchView(ClientRequiredMixin, generic.ListView):

    template_name = 'clients/clipping_search.html'

    def get(self, request, *args, **kwargs):
        action = request.GET.get('action')
        if action == 'excel':
            clipping_ids = request.GET.getlist('clipping')
            queryset = self.client.clippings.filter(pk__in=clipping_ids)
            content = export_clippings(self.client, queryset)
            response = HttpResponse(
                content, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            filename = f'Clippings.xlsx'
            filename = "filename*=utf-8''{}".format(quote(filename))
            response['Content-Disposition'] = f'attachment; {filename}'
            return response
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ClippingSearchForm(data=self.request.GET or None, client=self.client)
        return context

    def get_queryset(self):
        queryset = self.client.clippings.all()
        form = ClippingSearchForm(data=self.request.GET or None, client=self.client)
        return form.search(queryset)


class ClippingDetailView(ClientRequiredMixin, generic.DetailView):

    template_name = 'clients/clipping_detail.html'

    def get_queryset(self):
        return self.client.clippings.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RatingClippingForm(data=self.request.POST or None, instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=object)
        form = context['form']
        if form.is_valid():
            clipping = form.save(commit=False)
            clipping.has_evaluation = True
            clipping.save()
            messages.success(self.request, 'Avaliação atualizada com sucesso!')
        return self.render_to_response(context)


class ClippingDeleteView(AdminRequiredMixin, generic.View):

    def post(self, request, *args, **kwargs):
        queryset = Clipping.objects.filter(client__company=self.request.user.company)
        clipping = get_object_or_404(queryset, pk=self.kwargs['pk'])
        clipping.delete()
        messages.success(request, 'Clipping removido com sucesso!')
        return redirect('clients:clipping_list', slug=clipping.client.slug)


class ClippingDailyView(AdminRequiredMixin, ClientRequiredMixin, generic.ListView):
    template_name = 'clients/clipping_daily.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = self.client.clippings.all()

        if queryset.exists():
            # Start with today's date
            current_date = date.today()

            # If there are no clippings for the current date, search for the most recent day with clippings
            while not queryset.filter(publish_date__date=current_date).exists():
                current_date -= timedelta(days=1)
                # If the current_date goes beyond the date of the earliest clipping, break the loop
                try:
                    if current_date < queryset.earliest('publish_date').publish_date.date():
                        break
                except Clipping.DoesNotExist:
                    return queryset.none()

            queryset = queryset.filter(publish_date__date=current_date)

        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(client = self.client)
        context['clippings'] = self.get_queryset()
        return context


clipping_list = ClippingListView.as_view()
clipping_search = ClippingSearchView.as_view()
clipping_detail = ClippingDetailView.as_view()
clipping_delete = ClippingDeleteView.as_view()
clipping_daily = ClippingDailyView.as_view()
