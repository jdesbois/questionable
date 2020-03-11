from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.show_courses, name='courses'),
    path('course/', views.show_course, name='course'),
    path('course/lecture/', views.show_lecture, name='lecture'),
path('course/lecture/question', views.show_question, name='question'),
path('course/lecture/question/comment', views.show_comment, name='comment'),
path('course/lecture/question/reply', views.show_reply, name='reply'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)