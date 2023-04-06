from django.contrib import admin

from import_export.admin import ExportActionModelAdmin

from django_google_search.models import RequestSession, SearchResult

# Register your models here.
@admin.register(RequestSession)
class RequestSessionAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'date_filter', 'language_filter', 'request_user', 'created']
    fields = ['keyword', 'date_filter', 'language_filter', 'num_results']

    def save_model(self, request, obj, form, change):
        if not obj.request_user:
            obj.request_user = request.user

        super().save_model(request, obj, form, change)


class SearchResultAdmin(ExportActionModelAdmin):
    list_display = ['title', 'summary', 'keyword', 'request_user', 'request_date']
    list_filter = ['request_session__request_user', 'request_session__created']
    search_fields = ['request_session__keyword', 'title', 'summary']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(SearchResult, SearchResultAdmin)
