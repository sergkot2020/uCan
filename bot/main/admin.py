from django.contrib import admin
from .models import (
    RelationClientUser, Client, SystemMessageText, ClientGroup, AllowedChat
)

from django_json_widget.widgets import JSONEditorWidget
from django.contrib.postgres import fields


class RelationAdmin(admin.ModelAdmin):

    list_display = ['client', 'user']


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'avatar_tag', 'username', 'first_name', 'telegram_id', 'group']
    list_filter = ['username', 'first_name', 'telegram_id']
    search_fields = ['username', 'first_name', 'telegram_id']
    readonly_fields = ['avatar_tag']


class ClientGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'clients']
    list_filter = ['name']
    search_fields = ['name']


class SystemMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'text', 'caption', 'type', 'buttons', 'columns']
    list_filter = ['id', 'text', 'caption']
    search_fields = ['id', 'text', 'caption']
    readonly_fields = ('id',)
    formfield_overrides = {
        fields.JSONField: {'widget': JSONEditorWidget},
    }


class AllowedChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'chat']
    list_filter = ['id', 'chat']


admin.site.register(RelationClientUser, RelationAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ClientGroup, ClientGroupAdmin)
admin.site.register(SystemMessageText, SystemMessageAdmin)
admin.site.register(AllowedChat, AllowedChatAdmin)
admin.site.site_header = 'uCan bot'
