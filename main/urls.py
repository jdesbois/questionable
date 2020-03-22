from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.show_courses, name='courses'),
    path('contact_page/', views.contact_page, name='contact_page'),

    # User pages
    path('update_user/', views.update_user, name='update_user'),
    path('profile/', views.profile, name='profile'),
    path('set_role', views.set_role, name="set_role"),
    path('delete_user', views.delete_user, name='delete_user'),
    path('error', views.error, name='error'),
    path('set_role', views.set_role, name="set_role"),

    # Navigation/organization of content
    path('course/<slug:course_name_slug>/', views.show_course, name='course'),
    path('lecture/<slug:course_name_slug>/<slug:lecture_name_slug>/', views.show_lecture, name='lecture'),
    path('course/<slug:course_name_slug>/<slug:lecture_name_slug>/question/', views.show_question, name='question'),
    path('forum/<slug:course_name_slug>/<slug:forum_name_slug>/', views.show_forum, name='forum'),
    path('course/<slug:course_name_slug>/<slug:forum_name_slug>/post/', views.show_post, name='post'),

    # Form pages

    # Lecture pages
    path('courses/create_course', views.create_course, name='create_course'),
    path('course/<slug:course_name_slug>/create_lecture', views.create_lecture, name='create_lecture'),
    path('course/<slug:course_name_slug>/<slug:lecture_name_slug>/create_question/',
         views.create_question, name='create_question'),
    path('course/<slug:course_name_slug>/<slug:lecture_name_slug>/<slug:question_name_slug>/create_reply/',
         views.create_reply, name='create_reply'),
    path('upvote/',views.UpvoteQuestionView.as_view(), name='like_category'),

    # Forum pages
    path('course/<slug:course_name_slug>/create_forum/', views.create_forum, name='create_forum'),
    path('course/<slug:course_name_slug>/<slug:forum_name_slug>/create_post/', views.create_post, name='create_post'),
    path('course/<slug:course_name_slug>/<slug:forum_name_slug>/<slug:post_name_slug>/create_comment/',
         views.create_comment, name='create_comment'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)