from django.urls import path, re_path
from .views import *

urlpatterns = [
    re_path(r'', IndexView.as_view()),

#	path('', IndexView.as_view()),
#	path('<path:resource>', IndexView.as_view()),

]