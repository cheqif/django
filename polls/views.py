# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice,UserChoice
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
from django.db.models import Q


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        #列出有效的前50条问题
        return Question.objects.filter(is_active=1).order_by('-pub_date')[:50]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if question.max_select >= question.min_select:
        try:
            #selected_choices = question.choice_set.get(pk=','.join(request.POST.getlist('check_box_list')))
            selected_choices = ','.join(request.POST.getlist('check_box_list'))
            print(selected_choices)
        except (KeyError, Choice.DoesNotExist):

            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "你未做出选择.",
            })
        else:
            #先取用户查看是否已经就该问题投票，如果已经投票则不允许重复投票
            if request.user.id:
                is_voted = UserChoice.objects.filter(Q(user_id=request.user.id)&Q(question_id=question_id))
            else:
                is_voted = True
            if not is_voted:
                #计算一共选了几个答案
                # 所选答案计数
                checkeval = len(selected_choices.split(','))
                print(checkeval)
                #如果所选答案数不在在选择范围内，或者没选，报错
                if checkeval < question.min_select or checkeval > question.max_select or len(selected_choices) == 0:
                    return render(request, 'polls/detail.html', {
                        'question': question,
                        'error_message': "所选项目个数与要求不符.",
                    })
                else:
                    for choiceId in selected_choices.split(','):
                        print(choiceId)
                        selected_choice = question.choice_set.get(pk=choiceId)
                        print(selected_choice)
                    #需增加一个事务处理，先投票再记录投票人员是否已经就该问题投票
                        selected_choice.votes += 1
                        selected_choice.save()
                        user_choice = UserChoice(user_id=request.user.id,choice_id=selected_choice.id,question_id=question_id)
                        user_choice.save()

                        # Always return an HttpResponseRedirect after successfully dealing
                        # with POST data. This prevents data from being posted twice if a
                        # user hits the Back button.
                    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
            else:
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "你已经投过票了.",
                })
    else:
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "最少选择数大于最多选择数，请联系管理员重新设置.",
        })



# 登录
#使用自带的auth_user表作为用户表
def login(request):
    if request.method == 'GET':
        return render(request, 'polls/login.html')
    elif request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('pwd')
        # 调用auth.authenticate()方法进行登录校验
        user_obj = auth.authenticate(username=username, password=password)
        print(user_obj)
        if user_obj:
            auth.login(request, user_obj)
            return HttpResponseRedirect(reverse('polls:list'))
        else:
            return HttpResponseRedirect(reverse('polls:login'))




def list(request):
    questions_list = Question.objects.filter(is_active=1, start_date__lte=timezone.now(),  end_date__gte=timezone.now())
    paginator = Paginator(questions_list, 10) # 3 posts in each page
    page = request.GET.get('page')
    try:
        questions = paginator.get_page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        questions = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        questions = paginator.page(paginator.num_pages)
    return render(request,'polls/list.html',{'questions_list': questions})


def polls_settings(request):
    return {
        'polls_site_name': settings.SITE_NAME,
    }