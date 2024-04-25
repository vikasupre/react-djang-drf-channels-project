from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter()
router.register('api/server/select', views.ServerListViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
# Only include the media URL if DEBUG is True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
