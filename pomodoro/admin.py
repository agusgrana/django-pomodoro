from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from pomodoro.models import Favorite, Pomodoro


class PomodoroAdmin(admin.ModelAdmin):
    def _completed(self, obj):
        return obj.completed
    _completed.short_description = _('end time')

    list_display = ('title', 'category', 'duration', 'created', '_completed', 'owner',)
    list_filter = ('owner', 'category',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'duration', 'owner')
    list_filter = ('owner', 'category',)

admin.site.register(Pomodoro, PomodoroAdmin)
admin.site.register(Favorite, FavoriteAdmin)
