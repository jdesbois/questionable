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
    path('course/forum/', views.show_forum, name='forum'),
    path('course/forum/post', views.show_post, name='post'),
    # Form pages
    path('courses/create_course', views.create_course, name='create_course'),
    path('course/create_lecture', views.create_lecture, name='create_lecture'),
    path('course/lecture/create_question', views.create_question, name='create_question'),
    path('course/lecture/question/create_reply', views.create_reply, name='create_reply'),
    path('course/create_forum', views.create_forum, name='create_forum'),
    path('course/forum/create_post', views.create_post, name='create_post'),
    path('course/forum/post/create_comment', views.create_comment, name='create_reply'),
    path('contact_page/', views.contact_page, name='contact_page'),
    path('update_user/', views.update_user, name='update_user'),
    path('profile/', views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)