from django.contrib import admin

from import_export.admin import ExportActionModelAdmin
from import_export.resources import ModelResource
from import_export.fields import Field

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

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(request_user=request.user)


class SearchResultResource(ModelResource):
    user = Field()
    keyword = Field()
    search_date = Field()

    class Meta:
        model = SearchResult
        export_order = [
            'id', 'url', 'title', 'summary',
            'request_session', 'user', 'keyword',
            'search_date'
        ]

    def dehydrate_user(self, search_result):
        return search_result.request_session.request_user.username

    def dehydrate_keyword(self, search_result):
        return search_result.request_session.keyword

    def dehydrate_search_date(self, search_result):
        return str(search_result.request_session.created)


class SearchResultAdmin(ExportActionModelAdmin):
    list_display = ['title', 'summary', 'keyword', 'request_user', 'request_date']
    list_filter = ['request_session__request_user', 'request_session__created']
    search_fields = ['request_session__keyword', 'title', 'summary']
    resource_class = SearchResultResource

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        if request.user.is_superuser:
            return qs

        return qs.filter(request_session__request_user=request.user)

admin.site.register(SearchResult, SearchResultAdmin)
