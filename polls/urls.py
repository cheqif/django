from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('polls/index/', views.IndexView.as_view(), name='index'),
    path('', views.login, name='login'),
    path('polls/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
    path('polls/list/', views.list, name='list'),
]
