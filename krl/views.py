from django.http import HttpResponse
from django.views.decorators.cache import never_cache


@never_cache
def index(request):
    return HttpResponse("Terveh muailma!")