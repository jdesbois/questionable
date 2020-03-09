from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context_dict = {'message': 'Message sent from the view'}
    return render(request, 'main/index-mainpage.html', context=context_dict)


def user_profile_page(request):
    return render(request)


def course_list(request):

    context_dict = {}

    return


def questions_page(request):
    return


def user_login(request):
    return


def contact_page(request):
    return


def create_course(request):
    return


def create_lecture(request):
    return


def create_reply(request):
    return


def create_comment(request):
    return


def profile(request):
    return render(request, 'registration/profile.html')
