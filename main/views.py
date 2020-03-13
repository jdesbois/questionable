from django.shortcuts import redirect, render
from main.forms import LectureForm, CourseForm, QuestionForm, CommentForm, ReplyForm, UserForm, ProfileForm
from main.models import Course, Lecture, Question, Reply, Comment, Upvote, Enrollment, Post, Student, Tutor
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User, Group

# DISPLAY VIEWS


def index(request):
    context_dict = {'message': 'Message sent from the view'}
    return render(request, 'main/index-mainpage.html', context=context_dict)


def show_courses(request):
    context_dict = {}
    courses = Course.objects.all()
    context_dict['Courses'] = courses
    return render(request, 'main/courses.html', context=context_dict)


def show_course(request, selected_course):
    context_dict = {}

    try:
        course = Course.objects.get(selected_course)
        lecture_list = Lecture.objects.filter(course=selected_course)
        context_dict['course'] = course
        context_dict['lectures'] = lecture_list

    except Course.DoesNotExist:
        context_dict['course'] = None
        context_dict['lectures'] = None
    return render(request, 'main/course.html', context=context_dict)


@login_required
@permission_required('main.view_lecture')
def show_lectures(request):
    context_dict = {}
    lectures = Lecture.objects.all()
    context_dict['Lectures'] = lectures

    return render(request, 'main/lectures.html', context=context_dict)


def show_lecture(request, selected_lecture):
    context_dict = {}

    try:
        lecture = Lecture.objects.get(selected_lecture)
        comment_list = Comment.objects.filter(lecture=selected_lecture)
        reply_list = Reply.objects.filter(lecture=selected_lecture)
        context_dict['lecture'] = lecture
        context_dict['comments'] = comment_list
        context_dict['reply'] = reply_list

    except Lecture.DoesNotExist:
        context_dict['lecture'] = None
        context_dict['comments'] = None
        context_dict['reply'] = None
    return render(request, 'main/course/lecture.html', context=context_dict)


def show_question(request, selected_question):
    context_dict = {}

    try:
        question = Question.objects.get(selected_question)
        comment_list = Comment.objects.filter(question=selected_question)
        reply_list = Reply.objects.filter(question=selected_question)
        upvotes = Upvote.objects.filter(question=selected_question)
        context_dict['question'] = question
        context_dict['comments'] = comment_list
        context_dict['replies'] = reply_list
        context_dict['upvotes'] = upvotes

    except Question.DoesNotExist:
        context_dict['question'] = None
        context_dict['comments'] = None
        context_dict['replies'] = None
        context_dict['upvotes'] = None

    return render(request, 'main/course/lecture/question.html', context=context_dict)


def show_comment(request, selected_comment):
    context_dict = {}

    try:
        comment = Comment.objects.get(selected_comment)
        context_dict['comment'] = comment

    except Comment.DoesNotExist:
        context_dict['comment'] = None

    return render(request, 'main/course/lecture/question/comment.html', context=context_dict)


def show_reply(request, selected_reply):
    context_dict = {}

    try:
        comment = Reply.objects.get(selected_reply)
        context_dict['reply'] = comment

    except Reply.DoesNotExist:
        context_dict['reply'] = None

    return render(request, 'main/course/lecture/question/reply.html', context=context_dict)


def contact_page(request):
    return render(request, 'main/contact_page.html')

# View to generate profile page for logged in user (requires login)
@login_required(login_url='/accounts/login/')
def profile(request):

    current_user = request.user
    check_user(current_user)
    # context_dict = {}
    
    # try:
    #     student = Student.objects.get(user=current_user)
    #     questions = Question.objects.filter(user=student)
    #     posts = Post.objects.filter(user=student)
    #     context_dict['questions'] = questions
    #     context_dict['student'] = True
    #     context_dict['posts'] = posts

    # except:
    #     context_dict = {}

    return render(request, 'main/profile.html')


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
            return redirect('/main/courses')

        else:

            print(form.errors)

    return render(request, 'main/courses/create_course.html', {'form': form})


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

            return redirect('/main/course')

        else:

            print(form.errors)

    return render(request, 'main/course/create_lecture.html', {'form': form})


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

            return redirect('/main/course/lecture')

        else:

            print(form.errors)

    return render(request, 'main/course/lecture/create_question.html', {'form': form})


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
            return redirect('/main/course/lecture/question')

        else:

            print(form.errors)

    return render(request, 'main/course/lecture/question/create_reply.html', {'form': form})


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

            return redirect('/main/course/lecture/question')

        else:

            print(form.errors)

    return render(request, 'main/course/lecture/question/create_comment.html', {'form': form})


@login_required
def create_upvote(request, question, user):

    upvote = None

    # If user upvotes question
    if request.method == 'POST':
        upvote = Upvote()
        upvote.question = question
        upvote.user = user

    return render(request, 'main/course/lecture/question', {'upvote': upvote})


@login_required
def enroll_user(request, user, course):

    enroll = None

    # If user enrolls in course
    if request.method == 'POST':
        enroll = Enrollment()
        enroll.course = course
        enroll.user = user

    return render(request, 'main/courses', {'enrollment': enroll})

@login_required
@transaction.atomic
def update_user(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was sucessfull updated!'))
        else:
            messages.error(request, ('Please correct the error(s) below:'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'main/update_user.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def check_user(current_user):
    try:
        Student.objects.get(user=current_user)
        print(1)
        return 1
    except:
        try:
            Tutor.objects.get(user=current_user)
            print(2)
            return 2
        except:
            print(-1)
            return -1

    
    