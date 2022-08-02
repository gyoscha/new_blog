from django.contrib import admin
from django.contrib.auth.models import Group, User

from . import models


class ProfileInline(admin.StackedInline):
    """ Добавляем модель профиля в админку, чтобы они были на одной странице """
    model = models.Profile


class UserAdmin(admin.ModelAdmin):
    """ Меняем представление User в админке """
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


@admin.register(models.Note)
class NoteAdmin(admin.ModelAdmin):
    pass
