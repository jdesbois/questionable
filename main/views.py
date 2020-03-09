from django.http import HttpResponse
from django.shortcuts import render

def index(request):

    context_dict = {'message': 'Message sent from the view'}

    return render(request, 'main/index.html', context=context_dict)


def userProfilePage(request):
    
    return render(request)

def courseList(request):
    
    return
    
def questionsPage(request):
    
    return 

def login(request):
    
    return

def contactPage(request):
    
    return