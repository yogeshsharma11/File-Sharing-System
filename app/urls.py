from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *
from .  import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download/<uid>/' ,download),
    path('handle', HandleFileUploade.as_view()),
    path('api/upload/', HandleFileUploade.as_view(), name='file-upload')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()