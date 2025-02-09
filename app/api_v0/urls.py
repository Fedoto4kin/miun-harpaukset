from rest_framework.routers import DefaultRouter
from .lexiconViews import *
from .lessonsViews import *
from django.urls import include, path, re_path

router = DefaultRouter()
router.register(r'lexicon/pos', PosViewSet, basename='pos')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'modules', ModuleViewSet, basename='module')

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
    path(
        'lexicon/word-card/<int:word_id>/',
        WordCardView.as_view(),
        name='word-card'
    ),
    re_path(r'^lexicon/search/$', SearchViewList.as_view(), name='search-view'),
    re_path(r'^lexicon/reverse/$', SearchReverseViewList.as_view(), name='search-reverse-view'),
    path('modules/<int:module_id>/content/', ModuleContentView.as_view(), name='module-content'),
]
