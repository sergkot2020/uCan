from django.contrib import admin
from .models import Report, ReportForDetail, Anketa


class ReportAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'created', 'client', 'question_text', 'answer_options', 'answer']
    list_filter = ['question_id', 'created', 'client', 'answer']
    search_fields = ['client', 'answer']


class ReportDetailAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'created', 'client', 'question_text', 'answer']
    list_filter = ['question_id', 'created', 'client', 'answer']
    search_fields = ['client', 'answer']


class AnketaAdmin(admin.ModelAdmin):
    list_display = ['created', 'client', 'question', 'answer']
    list_filter = ['created', 'client', 'question']
    search_fields = ['client', 'question']


admin.site.register(Report, ReportAdmin)
admin.site.register(Anketa, AnketaAdmin)
admin.site.register(ReportForDetail, ReportDetailAdmin)
