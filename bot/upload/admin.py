from django.contrib import admin
from .models import FileLoader


class FileLoaderAdmin(admin.ModelAdmin):

    list_display = ['file']
    list_filter = ['file']
    search_fields = ['file']


admin.site.register(FileLoader, FileLoaderAdmin)