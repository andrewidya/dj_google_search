from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class RequestSession(models.Model):
    DATE_FILTER = (
        ('', 'None'),
        ('h1', 'Past Hour'),
        ('d1', 'Past 24 Hour'),
        ('d7', 'Past Week'),
        ('m1', 'Past Month'),
        ('y1', 'Past Year')
    )

    LANGUAGE_FILTER = (
        ("id", "Indonesia"),
        ("en", "English")
    )

    created = models.DateTimeField(
        verbose_name=_("Created"),
        auto_now_add=True,
        null=True,
        blank=True
    )
    keyword = models.CharField(verbose_name=_("Keyword"), max_length=254)
    num_results = models.IntegerField(verbose_name=_("Num Results"), default=10)
    date_filter = models.CharField(
        verbose_name=_("Date Filter"),
        max_length=4,
        choices=DATE_FILTER,
        null=True,
        blank=True)
    language_filter = models.CharField(
        verbose_name=_("Language Filter"),
        max_length=4,
        choices=LANGUAGE_FILTER,
        default="id"
    )
    request_user = models.ForeignKey(
        User,
        verbose_name=_("Request User"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"{self.keyword}, {self.date_filter}"

    class Meta:
        verbose_name = _("Request Session")
        verbose_name_plural = _("Request Session List")


class SearchResult(models.Model):
    url = models.URLField(verbose_name=_("URL"), null=True, blank=True)
    title = models.TextField(verbose_name=_("Title"), null=True, blank=True)
    summary = models.TextField(verbose_name=_("Summary"), null=True, blank=True)
    request_session = models.ForeignKey(
        RequestSession,
        verbose_name=_("Request Session"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"title: {self.title}, url: {self.url}"

    @property
    def request_user(self):
        return self.request_session.request_user

    @property
    def keyword(self):
        return self.request_session.keyword

    @property
    def request_date(self):
        return self.request_session.created

    class Meta:
        verbose_name = _("Search Result")
        verbose_name_plural = _("Search Result List")
