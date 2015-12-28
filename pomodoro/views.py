import datetime
import logging

import pytz
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import View
from icalendar import Calendar, Event
from pomodoro import __version__, __homepage__

from pomodoro.models import Pomodoro

try:
    from rest_framework.authtoken.models import Token
except ImportError:
    pass

logger = logging.getLogger(__name__)


class PomodoroCalendarView(View):
    limit = 7

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            try:
                token = Token.objects.select_related('user').get(key=request.GET.get('token'))
                if token:
                    request.user = token.user
                else:
                    return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            except Exception:
                logger.error('Invalid Token')
                return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

        cal = Calendar()
        cal.add('prodid', '-//Pomodoro Calendar//')
        cal.add('version', '2.0')
        cal.add('X-WR-CALNAME', 'Pomodoro for {0}'.format(request.user.username))
        cal.add('X-ORIGINAL-URL', request.build_absolute_uri())
        cal.add('X-GENERATOR', __homepage__)
        cal.add('X-GENERATOR-VERSION', __version__)

        today = datetime.datetime.utcnow()
        query = today - datetime.timedelta(days=self.limit)
        pomodoros = Pomodoro.objects.order_by('-created').filter(
            owner=request.user,
            created__gte=query,
        )

        for pomodoro in pomodoros:
            event = Event()
            event.add('summary', '{0} #{1}'.format(pomodoro.title, pomodoro.category))
            event.add('dtstart', pomodoro.created)
            event.add('dtend', pomodoro.created + datetime.timedelta(minutes=pomodoro.duration))
            event['uid'] = pomodoro.id
            cal.add_component(event)

        return HttpResponse(
            content=cal.to_ical(),
            content_type='text/plain; charset=utf-8'
        )