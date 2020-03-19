from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.show_courses, name='courses'),
    path('contact_page/', views.contact_page, name='contact_page'),
    path('update_user/', views.update_user, name='update_user'),
    path('profile/', views.profile, name='profile'),
    path('course/<slug:course_name_slug>/', views.show_course, name='course'),
    path('course/<slug:course_name_slug>/', views.show_courses, name='course'),
    path('course/<slug:course_name_slug>/<slug:lecture_name_slug>/', views.show_lecture, name='lecture'),
    path('course/<slug:course_name_slug>/<slug:lecture_name_slug>/question/', views.show_question, name='question'),
    path('course/<slug:course_name_slug>/<slug:forum_name_slug>/', views.show_forum, name='forum'),
    path('course/<slug:course_name_slug>/<slug:forum_name_slug>/post/', views.show_post, name='post'),
    # Form pages
    path('courses/create_course', views.create_course, name='create_course'),
    path('course/<slug:course_name_slug>/create_lecture', views.create_lecture, name='create_lecture'),
    path('course/<slug:course_name_slug>/<slug:lecture_name_slug>/create_question',
         views.create_question, name='create_question'),
    path('course/<slug:course_name_slug>/<slug:lecture_name_slug>/question/create_reply',
         views.create_reply, name='create_reply'),
    path('course/<slug:course_name_slug>/create_forum', views.create_forum, name='create_forum'),
    path('course/<slug:course_name_slug>/<slug:forum_name_slug>/create_post', views.create_post, name='create_post'),
    path('course/<slug:course_name_slug>/<slug:forum_name_slug>/post/create_comment',
         views.create_comment, name='create_reply'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)