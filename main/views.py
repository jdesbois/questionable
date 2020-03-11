from django.shortcuts import render
from main.forms import LectureForm, CourseForm, QuestionForm, CommentForm, ReplyForm
from main.models import Course, Lecture, Question, Reply, Comment, Upvote, Enrollment
from django.contrib.auth.decorators import login_required, permission_required

# DISPLAY VIEWS


def index(request):
    context_dict = {'message': 'Message sent from the view'}
    return render(request, 'main/index-mainpage.html', context=context_dict)


def show_courses(request):
    context_dict = {}
    courses = Course.objects.all()
    context_dict['Courses'] = courses


def show_course(request, selected_course):
    context_dict = {}
    lecture_list = {}

    try:
        course = Course.objects.get(selected_course)
        context_dict['course'] = course

    except Course.DoesNotExist:
        context_dict['course'] = None

    # Loops through all lectures to find those associated with this course
    for lecture in Lecture.objects.all():
        if lecture.course != selected_course:
            lecture_list += lecture

    context_dict['lectures'] = lecture_list
    return render(request, 'main/course.html', context=context_dict)


# @login_required
# @permission_required('main.view_lecture')
# def show_lectures(request):
#     context_dict = {}
#     lectures = Lecture.objects.all()
#     context_dict['Lectures'] = lectures
#
#     return render(request, 'main/lectures.html', context=context_dict)


def show_lecture(request, selected_lecture):
    context_dict = {}

    try:
        lecture = Lecture.objects.get(selected_lecture)
        context_dict['lecture'] = lecture

    except Lecture.DoesNotExist:
        context_dict['lecture'] = None

    return render(request, context=context_dict)


# def show_questions(request):
#     context_dict = {}
#     questions = Question.objects.all()
#     context_dict['Questions'] = questions


def show_question(request, selected_question):
    context_dict = {}

    try:
        question = Question.objects.get(selected_question)
        context_dict['question'] = question

    except Question.DoesNotExist:
        context_dict['question'] = None

    return render(request, context=context_dict)


# def show_comments(request):
#     context_dict = {}
#     comments = Comment.objects.all()
#     context_dict['Comments'] = comments


def show_comment(request, selected_comment):
    context_dict = {}

    try:
        comment = Comment.objects.get(selected_comment)
        context_dict['comment'] = comment

    except Comment.DoesNotExist:
        context_dict['comment'] = None

    return render(request, context=context_dict)


def contact_page(request):
    return


@login_required(login_url='/accounts/login/')
def profile(request):
    return render(request, 'registration/profile.html')


# CREATION VIEWS


@login_required
def create_course(request):
    form = CourseForm()

    # If user inputs comment
    if request.method == 'POST':
        form = CourseForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            form.save(commit=True)

            return # Needs redirect

        else:

            print(form.errors)

@login_required
def create_lecture(request, course):
    form = LectureForm()

    # If user inputs comment
    if request.method == 'POST':
        form = LectureForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            lecture = form.save(commit=True)
            lecture.course = course

            return # Needs redirect

        else:

            print(form.errors)

@login_required
def create_reply(request, user, question):
    form = ReplyForm()

    # If user inputs comment
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            reply = form.save(commit=True)
            reply.user = user
            reply.question = question
            return # Needs redirect

        else:

            print(form.errors)


@login_required
def create_comment(request, user, question):
    form = CommentForm()

    # If user inputs comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            comment = form.save(commit=True)
            comment.question = question
            comment.user = user

            return # Needs redirect

        else:

            print(form.errors)


@login_required
def create_question(request, lecture, user):
    form = QuestionForm()

    # If user inputs comment
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            question = form.save(commit=True)
            question.lecture = lecture
            question.user = user


@login_required
def create_upvote(request, question, user):

    # If user upvotes question
    if request.method == 'POST':
        upvote = Upvote()
        upvote.question = question
        upvote.user = user
    context_dict = {'upvote': upvote}
    return render(request, context=context_dict)


@login_required
def enroll_user(request, user, course):

    # If user enrolls in course
    if request.method == 'POST':
        enroll = Enrollment()
        enroll.course = course
        enroll.user = user
    context_dict = {'enrollment': enroll}
    return render(request, context=context_dict)