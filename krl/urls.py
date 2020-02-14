from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from krl import views

urlpatterns = [
    
    
    path('admin/', admin.site.urls),
    path('api/v0/', include('api_v0.urls')),
    path('', include('main.urls')),
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
#    path('lexicon/', include('main.urls')),
]

if settings.DEBUG and 'debug_toolbar' in settings.INSTALLED_APPS:
    import debug_toolbar
    urlpatterns += [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ]
