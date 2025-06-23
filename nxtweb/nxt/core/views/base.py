import datetime as dt

from dateutil.relativedelta import relativedelta

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.shortcuts import redirect

from nxt.clients.models import Clipping


class IndexView(LoginRequiredMixin, generic.TemplateView):

    template_name = 'index.html'

    @property
    def clipping_data(self):
        _clipping_data = getattr(self, '_clipping_data', None)
        if _clipping_data is None:
            today = dt.date.today()
            next_month = today + relativedelta(months=1)
            next_month = dt.datetime(next_month.year, next_month.month, 1)
            start_week = today - dt.timedelta(days=today.weekday())
            end_week = start_week + dt.timedelta(days=6)
            start_week = dt.datetime(start_week.year, start_week.month, start_week.day)
            end_week = dt.datetime(end_week.year, end_week.month, end_week.day, 23, 59, 59)
            company = self.request.user.company
            clippings = Clipping.objects.filter(client__company=company)
            gazette_clippings = clippings.filter(source__media__source__source_type='diariooficial')
            radio_clippings = clippings.filter(source__media__source__source_type='radio')
            tv_clippings = clippings.filter(source__media__source__source_type='tv')
            site_clippings = clippings.filter(source__media__source__source_type='site')
            _clipping_data = {
                'total': clippings.count(),
                'gazette': {
                    'total': gazette_clippings.count(),
                    'week': gazette_clippings.filter(
                        source__media__publish_date__gte=start_week,
                        source__media__publish_date__lte=end_week,
                    ).count(),
                    'month': gazette_clippings.filter(
                        source__media__publish_date__month=today.month,
                        source__media__publish_date__lt=next_month,
                    ).count(),
                },
                'radio': {
                    'total': radio_clippings.count(),
                    'week': radio_clippings.filter(
                        source__media__publish_date__gte=start_week,
                        source__media__publish_date__lte=end_week,
                    ).count(),
                    'month': radio_clippings.filter(
                        source__media__publish_date__month=today.month,
                        source__media__publish_date__lt=next_month,
                    ).count(),
                },
                'tv': {
                    'total': tv_clippings.count(),
                    'week': tv_clippings.filter(
                        source__media__publish_date__gte=start_week,
                        source__media__publish_date__lte=end_week,
                    ).count(),
                    'month': tv_clippings.filter(
                        source__media__publish_date__month=today.month,
                        source__media__publish_date__lt=next_month,
                    ).count(),
                },
                'site': {
                    'total': site_clippings.count(),
                    'week': site_clippings.filter(
                        source__media__publish_date__gte=start_week,
                        source__media__publish_date__lte=end_week,
                    ).count(),
                    'month': site_clippings.filter(
                        source__media__publish_date__month=today.month,
                        source__media__publish_date__lt=next_month,
                    ).count(),
                }
            }
            last_week = dt.datetime.now() - dt.timedelta(days=7)
            lastest_clippings = clippings.filter(source__media__publish_date__gte=last_week)
            lastest_clippings = lastest_clippings.annotate(
                created_date=TruncDate('source__media__publish_date')
            )
            lastest_clippings = lastest_clippings.values('created_date').annotate(total=Count('id'))
            lastest_clippings = lastest_clippings.order_by('created_date')
            _clipping_data['lastest_clippings'] = [
                {'x': u['created_date'].strftime('%Y-%m-%d'), 'y': u['total']} \
                    for u in lastest_clippings
            ]
            self._clipping_data = _clipping_data
        return _clipping_data


    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and self.request.user.profile == 'cliente':
            return redirect('clients:clipping_list')
        return super().dispatch(request, *args, **kwargs)


index = IndexView.as_view()
