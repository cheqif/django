# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from .models import Survey, SurveyChoice, SurveyQuestion, SurveyUser, SurveyUserChoice
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.contrib  import  auth#引入auth模块
from django.contrib.auth.models import User # auth应用中引入User类
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger  # 分页
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError


class DetailView(generic.DetailView):
    model = Survey
    template_name = 'survey/detail.html'


class ResultsView(generic.DetailView):
    model = Survey
    template_name = 'survey/results.html'


class MyResultsView(generic.DetailView):
    model = Survey
    template_name = 'survey/myresults.html'


def vote(request, survey_id):
    checklist = ''
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.user.id:
        is_voted = SurveyUserChoice.objects.filter(Q(user_id=request.user.id) & Q(survey_id=survey_id))
    else:
        is_voted = True
    if not is_voted:
        survey_question_list = SurveyQuestion.objects.raw('select id from survey_surveyquestion where survey_id='+str(survey_id))
        for survey_question_id in survey_question_list:
            survey_question = get_object_or_404(SurveyQuestion, pk=int(survey_question_id.id))
            if survey_question.max_select >= survey_question.min_select:
                try:
                    # selected_choices = question.choice_set.get(pk=','.join(request.POST.getlist('check_box_list')))
                    selected_choices = ','.join(request.POST.getlist('check_box_list'+str(survey_question.id)))
                    print(selected_choices)
                except (KeyError, SurveyChoice.DoesNotExist):

                    # Redisplay the question voting form.
                    return render(request, 'survey/detail.html', {
                        'survey': survey,
                        'error_message': survey_question.question_text+"你未做出选择.",
                    })
                else:
                    checkeval = len(selected_choices.split(','))
                    print(checkeval)
                    # 如果所选答案数不在在选择范围内，或者没选，报错
                    if checkeval < survey_question.min_select or checkeval > survey_question.max_select or len(selected_choices) == 0:
                        obj_list = request.POST
                        return render(request, 'survey/detail.html', {
                            'survey': survey, 'obj_list': obj_list,
                            'error_message': survey_question.question_text+"所选项目个数与要求不符.",
                             })
            else:
                return render(request, 'survey/detail.html', {
                    'survey': survey,
                    'error_message': survey_question.question_text+"最少选择数大于最多选择数，请联系管理员重新设置.",
                })
        for survey_question_id in survey_question_list:
            survey_question = get_object_or_404(SurveyQuestion, pk=int(survey_question_id.id))
            try:
                # selected_choices = question.choice_set.get(pk=','.join(request.POST.getlist('check_box_list')))
                selected_choices = ','.join(request.POST.getlist('check_box_list'+str(survey_question.id)))
                print(selected_choices)
            except (KeyError, SurveyChoice.DoesNotExist):

                # Redisplay the question voting form.
                return render(request, 'survey/detail.html', {
                    'survey': survey,
                    'error_message': survey_question.question_text+"你未做出选择.",
                })
            else:
                checkeval = len(selected_choices.split(','))
                print(checkeval)
                for choiceId in selected_choices.split(','):
                    print(choiceId)
                    selected_choice = survey_question.surveychoice_set.get(pk=choiceId)
                    print(selected_choice)
                    # 需增加一个事务处理，先投票再记录投票人员是否已经就该问题投票
                    selected_choice.votes += 1
                    selected_choice.save()
                    survey_user_choice = SurveyUserChoice(user_id=request.user.id, choice_id=selected_choice.id,question_id=survey_question_id.id,survey_id=survey_id)
                    survey_user_choice.save()
        return HttpResponseRedirect(reverse('survey:results', args=(survey_id,)))
    else:
        return render(request, 'survey/detail.html', {
            'survey': survey,
            'error_message': "你已经完成该问卷调查了.",
        })



def list(request):
    #surveys_list = Survey.objects.filter(is_active=1, start_date__lte=timezone.now(),  end_date__gte=timezone.now())
    surveys_list = Survey.objects.raw('select id,survey_text,pub_date,is_active,user_id,end_date,start_date from survey_survey ss where ss.id in (select survey_id from survey_surveyuser where id in (SELECT surveyuser_id from survey_surveyuser_user where user_id='+str(request.user.id)+')) and is_active=1 and start_date<=NOW()and end_date>=NOW()')
    paginator = Paginator(surveys_list, 10) # 3 posts in each page
    page = request.GET.get('page')
    try:
        surveys = paginator.get_page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        surveys = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        surveys = paginator.page(paginator.num_pages)
    return render(request,'survey/list.html', {'surveys_list': surveys})


def survey_settings(request):
    return {
        'survey_site_name': settings.SITE_NAME,
    }


