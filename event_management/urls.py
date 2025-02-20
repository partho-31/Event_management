from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('site_controller/',include('site_controller.urls')),
    path('home/',include('task.urls')),
    path('',include('core.urls')),
    path('user/',include('user.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)