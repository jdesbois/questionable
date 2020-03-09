from django.http import HttpResponse
from django.shortcuts import render




def index(request):

    context_dict = {'message': 'Message sent from the view'}

<<<<<<< HEAD
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
=======
    return render(request, 'main/index-mainpage.html', context=context_dict)

def profile(request):
    
    return render(request, 'registration/profile.html')
>>>>>>> 86639f014ca4a69c9af9fdf10eae114d3832eb84
