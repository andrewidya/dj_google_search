# Generated by Django 4.2 on 2023-04-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_google_search', '0003_alter_requestsession_request_user_searchresult'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestsession',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created'),
        ),
    ]
