# Generated by Django 4.2 on 2023-04-05 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_google_search', '0002_requestsession_language_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestsession',
            name='request_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Request User'),
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL')),
                ('title', models.TextField(blank=True, null=True, verbose_name='Title')),
                ('summary', models.TextField(blank=True, null=True, verbose_name='Summary')),
                ('request_session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='django_google_search.requestsession', verbose_name='Request Session')),
            ],
            options={
                'verbose_name': 'Search Result',
                'verbose_name_plural': 'Search Result List',
            },
        ),
    ]
