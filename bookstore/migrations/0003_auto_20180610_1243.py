# Generated by Django 2.0.6 on 2018-06-10 12:43

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0002_auto_20180610_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='httprequest',
            name='request_cookies',
        ),
        migrations.AlterField(
            model_name='book',
            name='publish_date',
            field=models.DateField(default=datetime.datetime(2018, 6, 10, 12, 43, 49, 953176, tzinfo=utc)),
        ),
    ]
