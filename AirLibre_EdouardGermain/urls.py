"""
URL configuration for AirLibre_EdouardGermain project.

"""
from django.contrib import admin
from django.urls import path, include
from AirLibre_EdouardGermain import settings
from activities import views
from django.conf.urls.static import static
from django.views.static import serve


urlpatterns = [
    path('activities/', include('activities.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/', views.signup, name='signup'),
    path('', include('activities.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    ]



