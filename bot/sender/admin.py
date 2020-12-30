from django.contrib import admin
from .models import (
    FeedBackMessage, ContentMessage, OutgoingMessage, ButtonMessage,
    QuestionMessage, DetailedAnswer
)
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget
from django.forms import Textarea
from django.db import models
from django import forms
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin


class ClientInline(admin.TabularInline):
    model = FeedBackMessage.client.through
    extra = 3


class GroupInline(admin.TabularInline):
    model = FeedBackMessage.group.through
    extra = 3


class ButtonMessageInline(admin.StackedInline):
    model = ButtonMessage
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': EmojiPickerTextareaAdmin},
    }
    readonly_fields = ('file_id',)


class FeedBackMessageAdmin(admin.ModelAdmin):
    """
    Model for create content message.
    """
    list_display = [
        'title', 'send_now', 'is_delivered', 'time_to_send', 'responsible'
    ]
    exclude = ('client', 'group')
    inlines = [ButtonMessageInline, ClientInline, GroupInline]
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }


class ClientContentInline(admin.TabularInline):
    model = ContentMessage.client.through
    verbose_name = 'telegram user'
    verbose_name_plural = 'telegram users'
    extra = 3


class GroupContentInline(admin.TabularInline):
    model = ContentMessage.group.through
    verbose_name = 'group'
    verbose_name_plural = 'group'
    extra = 3


class MessageContentInline(admin.StackedInline):
    model = OutgoingMessage
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': EmojiPickerTextareaAdmin},
    }
    readonly_fields = ('file_id',)


class ContenMessageAdmin(admin.ModelAdmin):
    """
    Model for create content message.
    """
    list_display = [
        'title', 'send_now', 'is_delivered', 'time_to_send', 'responsible'
    ]
    exclude = ('client', 'group')
    inlines = [
        MessageContentInline, ClientContentInline, GroupContentInline
    ]


class ClientDetailedInline(admin.TabularInline):
    model = DetailedAnswer.client.through
    extra = 3


class GroupDetailedInline(admin.TabularInline):
    model = DetailedAnswer.group.through
    extra = 3


class QuestionInline(admin.StackedInline):
    model = QuestionMessage
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': EmojiPickerTextareaAdmin},
    }
    readonly_fields = ('file_id',)


class DetailedAnswerAdmin(admin.ModelAdmin):
    """
    Model for create content message.
    """
    list_display = [
        'title', 'send_now', 'is_delivered', 'time_to_send', 'responsible'
    ]
    exclude = ('client', 'group')
    inlines = [
        QuestionInline, ClientDetailedInline, GroupDetailedInline
    ]


admin.site.register(FeedBackMessage, FeedBackMessageAdmin)
admin.site.register(ContentMessage, ContenMessageAdmin)
admin.site.register(DetailedAnswer, DetailedAnswerAdmin)
