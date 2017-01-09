from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from pomodoro.models import Favorite, Pomodoro


class PomodoroAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start', 'end', 'duration', 'owner',)
    list_filter = ('owner', 'start', 'category',)


class FavoriteAdmin(admin.ModelAdmin):
    def _icon(self, obj):
        return True if obj.icon else False
    _icon.short_description = _('icon')
    _icon.boolean = True

    list_display = ('title', 'category', 'duration', 'owner', '_icon')
    list_filter = ('owner', 'category',)

admin.site.register(Pomodoro, PomodoroAdmin)
admin.site.register(Favorite, FavoriteAdmin)
