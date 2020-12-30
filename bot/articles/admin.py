from django.contrib import admin
from .models import Section, ArticleMessage, ArticleSendMessage


class SectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'callback']
    list_filter = ['id', 'title']
    readonly_fields = ['callback']


class ArticleMessageInline(admin.StackedInline):
    model = ArticleMessage
    extra = 1
    readonly_fields = ('file_id',)


class ArticleSendMessageAdmin(admin.ModelAdmin):
    """
    Model for create content message.
    """
    list_display = ['title', 'section']

    inlines = [ArticleMessageInline]


admin.site.register(Section, SectionAdmin)
admin.site.register(ArticleSendMessage, ArticleSendMessageAdmin)
