from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='questions-index'),
    path('<int:question_id>/hints/<int:hint_id>/vote/', views.vote, name='vote'),
    path('<int:question_id>/', views.question, name='question'),
    path('add_hint/', views.add_hint, name='add_hint'),
]
