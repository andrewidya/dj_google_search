from django.contrib import admin

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


@admin.register(SearchResult)
class SearchResult(admin.ModelAdmin):
    list_display = ['title', 'summary', 'request_session']

    def has_add_permission(self, request):
        return False

