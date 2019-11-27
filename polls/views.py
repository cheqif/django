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
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):

        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "你未做出选择.",
        })
    else:
        #先取用户查看是否已经就该问题投票，如果已经投票则不允许重复投票

        is_voted = UserChoice.objects.filter(Q(user_id=request.user.id)&Q(question_id=question_id))
        if not is_voted:
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
    questions_list = Question.objects.all()
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


