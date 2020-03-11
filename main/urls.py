from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('course/', views.show_course, name='course'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)