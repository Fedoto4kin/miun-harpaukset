from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import include, path, re_path

router = DefaultRouter()
router.register(r'lexicon/pos', PosViewSet, basename='pos')

urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^lexicon/search/(?P<search>[\w-]+)/$', SearchViewList.as_view(), name='search-view'),
    re_path(r'^lexicon/reverse/(?P<search>[\w-]+)/$', SearchReverseViewList.as_view(), name='search-reverse-view'),
]