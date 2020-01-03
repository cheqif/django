# Generated by Django 2.2.7 on 2019-12-26 01:27

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_text', models.CharField(max_length=2000, verbose_name='调查问卷')),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2019, 12, 26, 1, 27, 18, 752846, tzinfo=utc), verbose_name='发布时间')),
                ('is_active', models.CharField(choices=[('0', '失效'), ('1', '有效')], default='1', max_length=10, verbose_name='是否有效')),
                ('start_date', models.DateTimeField(default=datetime.datetime(2019, 12, 26, 1, 27, 18, 752846, tzinfo=utc), verbose_name='开始时间')),
                ('end_date', models.DateTimeField(default=datetime.datetime(2019, 12, 27, 1, 27, 18, 752846, tzinfo=utc), verbose_name='结束时间')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发布者')),
            ],
            options={
                'verbose_name': '调查问卷',
                'verbose_name_plural': '调查问卷',
            },
        ),
        migrations.CreateModel(
            name='SurveyChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_text', models.CharField(max_length=2000, verbose_name='选项')),
                ('votes', models.IntegerField(default=0, verbose_name='票数')),
            ],
            options={
                'verbose_name': '选项',
                'verbose_name_plural': '选项',
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=2000, verbose_name='问题')),
                ('min_select', models.PositiveIntegerField(default=1, verbose_name='最小选择数')),
                ('max_select', models.PositiveIntegerField(default=1, verbose_name='最大选择数')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Survey')),
            ],
            options={
                'verbose_name': '问题',
                'verbose_name_plural': '问题',
            },
        ),
        migrations.CreateModel(
            name='SurveyUserChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.SurveyChoice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.SurveyQuestion')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Survey')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Survey')),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '调查问卷准入机制',
                'verbose_name_plural': '调查问卷准入机制',
            },
        ),
        migrations.AddField(
            model_name='surveychoice',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.SurveyQuestion'),
        ),
    ]