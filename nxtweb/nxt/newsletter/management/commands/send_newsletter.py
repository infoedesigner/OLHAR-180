import datetime as dt

from django.utils import timezone
from django.core.management.base import BaseCommand
from django.conf import settings

from nxt.newsletter.models import Schedule, ScheduleHistory


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        timezone.activate(settings.TIME_ZONE)
        now = dt.datetime.now()
        time = now.time()
        schedules = Schedule.objects.filter(day=now.isoweekday(), time__lte=time)
        history = ScheduleHistory.objects.values('schedule')
        schedules = schedules.exclude(pk__in=history)
        for schedule in schedules:
            print(schedule)
            schedule.send_newsletter()
