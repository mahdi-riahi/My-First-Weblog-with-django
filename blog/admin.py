from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'datetime_updated', 'status',)
    ordering = ('-status', '-datetime_updated',)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('related_post', 'author', 'datetime_created')
    ordering = ('-datetime_created', )
