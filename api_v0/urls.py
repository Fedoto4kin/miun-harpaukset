from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import include, path, re_path


router = DefaultRouter()
router.register(r'lexicon/pos/?', PosViewSet, basename='pos')
router.register(r'lexicon', WordViewSet, basename='word')

router.urls.append(re_path('lexicon/search/(?P<search>.+)/?$', SearchViewList.as_view()))

urlpatterns = router.urls