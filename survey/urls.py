from django.urls import path

from . import views

app_name = 'survey'
urlpatterns = [
    path('survey/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('survey/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('survey/<int:pk>/myresults/', views.MyResultsView.as_view(), name='myresults'),
    path('survey/<int:survey_id>/vote/', views.vote, name='vote'),
    path('survey/list/', views.list, name='list'),
]
