from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'