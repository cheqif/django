import datetime

from django.db import models
from django.utils import timezone
from django.contrib  import  auth#引入auth模块
from django.contrib.auth.models import User # auth应用中引入User类
from django.core.exceptions import ValidationError


class Survey(models.Model):
    survey_text = models.CharField(max_length=2000, verbose_name="问卷调查")
    pub_date = models.DateTimeField(verbose_name="发布时间",default=timezone.now())
    is_active_CHOICES = (('0', '失效'), ('1', '有效'))
    is_active = models.CharField(max_length=10,choices=is_active_CHOICES,default='1', verbose_name="是否有效")
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="发布者")
    start_date = models.DateTimeField(verbose_name="开始时间",default=timezone.now())
    end_date = models.DateTimeField(verbose_name="结束时间",default=timezone.now()+datetime.timedelta(days=1))

    def __str__(self):
        return self.survey_text

    def surveys(self):
        return self.survey_text

    def pubdate(self):
        return self.pub_date

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def was_active(self):
        return self.get_is_active_display()

    def author_name(self):
        return self.user.username

    pubdate.short_description = '发布日期'
    surveys.short_description = '问卷调查'
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = '是否最近发布?'
    was_active.short_description = '是否有效?'
    author_name.short_description = '发布者'

    class Meta:
        verbose_name_plural = '问卷调查'
        verbose_name = '问卷调查'


class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=2000, verbose_name="问题")
    min_select = models.PositiveIntegerField(default=1, verbose_name="最小选择数")
    max_select = models.PositiveIntegerField(default=1, verbose_name="最大选择数")

    def __str__(self):
        return self.question_text

    def questions(self):
        return self.question_text

    questions.short_description = '问题'

    class Meta:
        verbose_name_plural = '问题'
        verbose_name = '问题'


class SurveyChoice(models.Model):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=2000,verbose_name="选项")
    votes = models.IntegerField(default=0, verbose_name="票数")

    def __str__(self):
        return self.choice_text

    def choices(self):
        return self.choice_text

    class Meta:
        verbose_name_plural = '选项'
        verbose_name = '选项'


class SurveyUserChoice(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(SurveyChoice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class SurveyUser(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user = models.ManyToManyField(User, verbose_name="用户")

    def __str__(self):
        return self.survey.survey_text

    class Meta:
        verbose_name_plural = '调查问卷准入机制'
        verbose_name = '调查问卷准入机制'
