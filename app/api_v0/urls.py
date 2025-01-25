from rest_framework.routers import DefaultRouter
from .lexiconViews import *
from .lessonsViews import *
from django.urls import include, path, re_path

router = DefaultRouter()
router.register(r'lexicon/pos', PosViewSet, basename='pos')
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'lexicon/search-suggestions/',
        SearchSuggestionsView.as_view(),
        name='search-suggestions'
    ),
    path(
        'lexicon/reverse-search-suggestions/',
        ReverseSearchSuggestionsView.as_view(),
        name='search-suggestions-reverse'
    ),
    re_path(r'^lexicon/search/$', SearchViewList.as_view(), name='search-view'),
    re_path(r'^lexicon/reverse/$', SearchReverseViewList.as_view(), name='search-reverse-view'),
]
