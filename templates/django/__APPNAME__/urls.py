from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.contrib import admin
from django.views.static import serve as static_serve
from decorator_include import decorator_include

urlpatterns = [
    url(r'^', include('landings.urls')),
    url(r'^', include('user_auth.urls')),
    # url(r'^myapp/', decorator_include(login_required, 'myapp.urls')),
    url(r'^adminweb/', include(admin.site.urls)),
]

urlpatterns += [
    url(r'^static/(?P<path>.*)$', static_serve, {
        'document_root': 'static'
    })
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
