# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ts.models


class Migration(migrations.Migration):

    dependencies = [
        ('ts', '0002_remove_usertestcaseanswer_isfinished'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestQuestions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', ts.models.ListField()),
                ('user_test_case_answer', models.ForeignKey(to='ts.UserTestCaseAnswer')),
            ],
        ),
    ]
