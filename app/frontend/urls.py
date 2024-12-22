from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('lexicon/', LexiconView.as_view(), name='lexicon'),
    path('lessons/', LessonsView.as_view(), name='lessons'),
    ]
