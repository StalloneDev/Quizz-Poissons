from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('result/<int:question_id>/', views.result, name='result'),
    path('end/<int:score>/<int:question_id>/', views.end_quiz, name='end_quiz'),
    
]
