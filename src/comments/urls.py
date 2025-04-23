from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:article_id>/', views.add_comment, name='add_comment'),
    path('reply/<int:comment_id>/', views.reply_comment, name='reply_comment'),
    path('vote/<int:comment_id>/<str:vote_type>/', views.vote_comment, name='vote_comment'),
]
