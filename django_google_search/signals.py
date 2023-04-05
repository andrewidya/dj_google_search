from django.db.models.signals import post_save
from django.dispatch import receiver

import django_rq

from django_google_search.models import RequestSession, SearchResult
from django_google_search.utils import search as google_search


@receiver(post_save, sender=RequestSession)
def run_search(sender, instance, created, *args, **kwargs):
    if not created:
        return

    params = {
        "lang": instance.language_filter,
    }

    if instance.date_filter:
        params.update({"date_filter": instance.date_filter})

    if instance.num_results:
        params.update({"num_results": instance.num_results})

    queue = django_rq.get_queue('default', is_async=True)
    queue.enqueue(search, instance.id, instance.keyword, params)


def search(request_session_id, keyword, params):
    results = google_search(keyword, **params)

    for result in results:
        if not result.url or not result.title:
            continue

        suffix_params_index = result.url.find("&sa=")
        url = (result.url[:suffix_params_index]).replace("/url?q=", "")

        request_session = RequestSession.objects.get(pk=request_session_id)
        search_result = SearchResult(
            title=result.title, url=url, summary=result.description, request_session=request_session)
        search_result.save()