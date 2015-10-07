from setuptools import find_packages, setup

from pomodoro import __version__

setup(
    name='django-pomodoro',
    description='Render Pomodoro Calendars',
    author='Paul Traylor',
    url='https://github.com/kfdm/django-pomodoro',
    version=__version__,
    packages=find_packages(),
    install_requires=['icalendar'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    entry_points={
        'powerplug.apps': ['pomodoro = pomodoro'],
        'powerplug.urls': ['pomodoro = pomodoro.urls'],
        'powerplug.rest': ['pomodoro = pomodoro.rest:PomodoroViewSet']
    },
)
