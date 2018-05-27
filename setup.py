from setuptools import find_packages, setup

from pomodoro import __version__, __homepage__

setup(
    name='django-pomodoro',
    description='Render Pomodoro Calendars',
    author='Paul Traylor',
    url=__homepage__,
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'djangorestframework',
        'icalendar',
        'Pillow',
        ],
    extras_require={
        'standalone': [
            'celery[redis]==4.0.2',
            'dj_database_url',
            'Django==2.0.5',
            'envdir',
            'prometheus_client',
            'psycopg2',
            'raven',
            'social-auth-app-django==2.1.0',
        ],
        'dev': [
            'unittest-xml-reporting',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    entry_points={
        'powerplug.apps': ['pomodoro = pomodoro.apps.PomodoroConfig'],
        'powerplug.urls': ['pomodoro = pomodoro.urls'],
        'powerplug.rest': [
            'pomodoro = pomodoro.rest:PomodoroViewSet',
            'favorite = pomodoro.rest:FavoriteViewSet',
        ],
        'console_scripts': [
            'pomodoro = pomodoro.standalone.manage:main[standalone]',
        ],
    },
)
