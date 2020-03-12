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
    path('courses/create_course', views.create_course, name='create_course'),
    path('course/create_lecture', views.create_lecture, name='create_lecture'),
    path('course/lecture/create_question', views.create_question, name='create_question'),
    path('course/lecture/question/create_reply', views.create_reply, name='reply'),
    path('course/lecture/question/create_comment', views.create_comment, name='reply'),
    path('contact_page/', views.contact_page, name='contact_page'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)