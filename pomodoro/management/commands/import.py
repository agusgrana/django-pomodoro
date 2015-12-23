import datetime

import pytz
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.backends.sqlite3.base import DatabaseWrapper
from pomodoro.legacy import NSTIMEINTERVAL
from pomodoro.models import Pomodoro


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--no-input', action='store_true')
        parser.add_argument('user')
        parser.add_argument('inputfile')
        parser.add_argument('tagfile', nargs='?')

    def handle(self, *args, **options):
        tags = {}
        if options['tagfile']:
            with open(options['tagfile']) as fp:
                for line in fp:
                    key, value = line.strip().split('=')
                    tags[key] = value

        user = User.objects.get(username=options['user'])
        pomodoros = Pomodoro.objects.filter(owner=user)
        if options['no_input'] is False:
            while len(pomodoros):
                self.stdout.write('Delete %d pomodoros for %s' % (len(pomodoros), user))
                if input('Confirm yes/no ').lower() == 'yes':
                    break
        pomodoros.delete()
        self.stdout.write('Importing Pomodoros')

        cursor = DatabaseWrapper(settings_dict={
            'NAME': options['inputfile'],
            'CONN_MAX_AGE': None,
            'OPTIONS': [],
            'AUTOCOMMIT': False,
        }).cursor()
        cursor.execute('SELECT cast(ZWHEN as integer), ZDURATIONMINUTES, ZNAME FROM ZPOMODOROS ')
        for zwhen, zminutes, zname in cursor.fetchall():
            seconds = zminutes * 60

            p = Pomodoro()
            p.title = zname
            p.owner = user
            #  p.start = datetime.datetime.fromtimestamp(zwhen + NSTIMEINTERVAL - seconds, pytz.utc)
            #  p.end = datetime.datetime.fromtimestamp(zwhen + NSTIMEINTERVAL, pytz.utc)
            p.created = datetime.datetime.fromtimestamp(zwhen + NSTIMEINTERVAL - seconds, pytz.utc)

            for word in p.title.split():
                if word.startswith('#'):
                    p.category = word.strip('#')
                    break

            if not p.category:
                for search, tag in tags.items():
                    if search in p.title:
                        p.category = tag
                        break

            p.duration = zminutes
            p.save()
            self.stdout.write('Added %s' % p)
