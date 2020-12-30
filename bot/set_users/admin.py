from django.contrib import admin
from .models import KeyNewUser, KeyForMailing


class KeyNewUserAdmin(admin.ModelAdmin):

    list_display = ['key_for_new_user']
    list_filter = ['key_for_new_user']
    search_fields = ['key_for_new_user']


class KeyForMailingAdmin(admin.ModelAdmin):

    list_display = ['key_for_mailing']
    list_filter = ['key_for_mailing']
    search_fields = ['key_for_mailing']


admin.site.register(KeyNewUser, KeyNewUserAdmin)
admin.site.register(KeyForMailing, KeyForMailingAdmin)
