from django.shortcuts import redirect, render
from main.forms import LectureForm, CourseForm, QuestionForm, CommentForm, ReplyForm, UserForm, ProfileForm, ForumForm, \
    PostForm
from main.models import Course, Lecture, Question, Reply, Comment, Upvote, Enrollment, Post, Student, Tutor, Forum
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.views import View
from django.http import HttpResponse

# DISPLAY VIEWS


@login_required
def home(request):
    return render(request, 'core/home.html')


def index(request):

    question_list = Question.objects.order_by('-upvote')[:3]
    question_new = Question.objects.order_by('upvote')[:3]
    
    context_dict = {}
    context_dict = {'message': 'Message sent from the view'}
    context_dict['questions'] = question_list
    context_dict['newquestions'] = question_new
    
    return render(request, 'main/index.html', context=context_dict)


def show_courses(request):
    context_dict = {}
    courses = Course.objects.all()
    context_dict['courses'] = courses
    return render(request, 'main/courses.html', context=context_dict)


def show_course(request, course_name_slug):
    context_dict = {}

    try:
        course = Course.objects.get(slug=course_name_slug)
        lecture_list = Lecture.objects.filter(course=course)
        forum_list = Forum.objects.filter(course=course)
        context_dict['course'] = course
        context_dict['lectures'] = lecture_list
        context_dict['forums'] = forum_list

    except Course.DoesNotExist:
        context_dict['course'] = None
        context_dict['lectures'] = None
        context_dict['forums'] = None
    return render(request, 'main/course_details.html', context=context_dict)


# @login_required
# @permission_required('main.view_lecture')
# def show_lectures(request):
#     context_dict = {}
#     lectures = Lecture.objects.all()
#     context_dict['lectures'] = lectures
#
#     return render(request, 'main/lectures.html', context=context_dict)


def show_lecture(request, course_name_slug, lecture_name_slug):
    context_dict = {}

    try:
        course = Course.objects.get(slug=course_name_slug)
        lecture = Lecture.objects.get(slug=lecture_name_slug)
        question_list = Question.objects.filter(lecture=lecture)
        form = QuestionForm()

        reply_dict = {}
        upvote_dict = {}

        for question in question_list:
            reply_dict[question.title] = Reply.objects.filter(question=question)
            upvote_dict[question.title] = Upvote.objects.filter(question=question).count()

        context_dict['course'] = course
        context_dict['lecture'] = lecture
        context_dict['questions'] = question_list
        context_dict['reply_dict'] = reply_dict
        context_dict['upvote_dict'] = upvote_dict
        context_dict['form'] = form

    except Lecture.DoesNotExist:
        context_dict['lecture'] = None
        context_dict['questions'] = None
        context_dict['reply_dict'] = None

    return render(request, 'main/lecture.html', context=context_dict)


def show_question(request):
    context_dict = {}

    try:
        question = request.question
        reply_list = Reply.objects.filter(question=question)
        upvotes = Upvote.objects.filter(question=question)
        context_dict['question'] = question
        context_dict['replies'] = reply_list
        context_dict['upvotes'] = upvotes

    except Question.DoesNotExist:
        context_dict['question'] = None
        context_dict['replies'] = None
        context_dict['upvotes'] = None

    return render(request, 'main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/question.html', context=context_dict)


# def show_reply(request):
#     context_dict = {}
#
#     try:
#         reply = request.reply
#         context_dict['reply'] = reply
#
#     except Reply.DoesNotExist:
#         context_dict['reply'] = None
#
#     return render(request, 'main/course/lecture/question/reply.html', context=context_dict)


def show_forum(request, forum_name_slug):
    context_dict = {}
    try:
        forum = Forum.objects.get(slug=forum_name_slug)
        post_list = Post.objects.filter(forum=forum)
        context_dict['forum'] = forum
        context_dict['posts'] = post_list
    except Forum.DoesNotExist:
        context_dict['forum'] = None
        context_dict['posts'] = None
    return render(request, 'main/course/<slug:course_name_slug>/forum.html', context=context_dict)


def show_post(request):
    context_dict = {}

    try:
        question = request.question
        comment_list = Reply.objects.filter(question=question)
        upvotes = Upvote.objects.filter(question=question)
        context_dict['forum'] = question
        context_dict['comments'] = comment_list
        context_dict['upvotes'] = upvotes

    except Post.DoesNotExist:
        context_dict['forum'] = None
        context_dict['comments'] = None
        context_dict['upvotes'] = None

    return render(request, 'main/course/<slug:course_name_slug>/<slug:forum_name_slug>/post.html', context=context_dict)


# def show_comment(request):
#     context_dict = {}
#
#     try:
#         comment = request.comment
#         context_dict['comment'] = comment
#
#     except Comment.DoesNotExist:
#         context_dict['comment'] = None
#
#     return render(request, 'main/course/lecture/question/comment.html', context=context_dict)

def contact_page(request):
    return render(request, 'main/contact_page.html')


# View to generate profile page for logged in user (requires login)
@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    context_dict = {}
    role = None
    questions = Question.objects.all()[:3]
    posts = Post.objects.all()[:3]
    replies = Reply.objects.all()[:3]
    context_dict['questions'] = questions
    context_dict['posts'] = posts
    context_dict['replies'] = replies
    
    if check_user(current_user) == 1:
        role = "Student"
    elif check_user(current_user) == 2:
        role ="Lecturer"
    else:
        role = None

    context_dict['role'] = role

    return render(request, 'main/profile.html', context=context_dict)


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
            return redirect('/main/courses/')

        else:

            print(form.errors)

    return render(request, 'main/create_course.html', {'form': form})


@login_required
def create_lecture(request, course_name_slug):

    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        course = None

    if course is None:
        return redirect('/main/course/<slug:course_name_slug>/')

    form = LectureForm()

    # If user inputs comment
    if request.method == 'POST':
        form = LectureForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            lecture = form.save(commit=False)
            lecture.course = course
            lecture.save()

            return redirect(reverse('main:course',
                                    kwargs={'course_name_slug': course_name_slug}))

        else:

            print(form.errors)

    context_dict = {'form': form, 'course': course}
    return render(request, 'main/create_lecture.html', context_dict)


@login_required
def create_question(request, course_name_slug, lecture_name_slug):

    # find lecture object
    try:
        lecture = Lecture.objects.get(slug=lecture_name_slug)
    except Lecture.DoesNoExist:
        lecture = None

    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        course = None

    if course is None or lecture is None:
        return redirect('/main/course/<slug:course_name_slug>/<slug:lecture_name_slug/')

    form = QuestionForm()

    # If user inputs comment
    if request.method == 'POST':
        print("after post")
        form = QuestionForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            question = form.save(commit=False)
            question.lecture = lecture
            # question.user = request.user
            question.save()

            # return redirect('/main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/')
            return redirect(reverse('main:lecture',
                                    kwargs={'course_name_slug': course_name_slug,
                                            'lecture_name_slug': lecture_name_slug}))
        else:
            print(form.errors)

    # why did we previously have to pass form here? Works without it for current setup?
    # return render(request, 'main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/', {'form': form})
    return redirect(reverse('main:lecture',
                            kwargs={'course_name_slug': course_name_slug,
                                    'lecture_name_slug': lecture_name_slug}))


class UpvoteQuestionView(View):
    # @method_decorator(login_required)
    def get(self, request):
        question_id = request.GET['question_id']

        # get question
        try:
            question = Question.objects.get(id=int(question_id))
        except Question.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        # create an upvote
        u = Upvote.objects.get_or_create(question=question)

        # if a new object is created
        if(u[1] == True):
            u[0].save()
        # else, this upvote has already been cast
        else:
            print("Object already exists")

        # count upvotes for given question
        count = Upvote.objects.filter(question=question).count()

        # return updated count
        return HttpResponse(count)


@login_required
def create_reply(request):
    form = ReplyForm()

    # If user inputs comment
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            reply = form.save(commit=True)
            reply.user = request.user
            reply.question = request.question
            return redirect('/main/course/lecture/question/')

        else:

            print(form.errors)

    return render(request, 'main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/question/', {'form': form})


@login_required
def create_forum(request):
    form = ForumForm()

    # If user inputs comment
    if request.method == 'POST':
        form = ForumForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            forum = form.save(commit=True)
            forum.course = request.course

            return redirect('/main/course/<slug:course_name_slug>/')

        else:

            print(form.errors)

    return render(request, 'main/course/<slug:course_name_slug>/', {'form': form})




@login_required
def create_post(request):
    form = PostForm()

    # If user inputs comment
    if request.method == 'POST':
        form = PostForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            post = form.save(commit=True)
            post.forum = request.forum
            post.user = request.user

            return redirect('/main/course/<slug:course_name_slug>/<slug:forum_name_slug>/')

        else:

            print(form.errors)

    return render(request, 'main/<slug:course_name_slug>/<slug:course_name_slug>/', {'form': form})


@login_required
def create_comment(request):
    form = CommentForm()

    # If user inputs comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            comment = form.save(commit=True)
            comment.post = request.post
            comment.user = request.user

            return redirect('/main/course/<slug:course_name_slug>/<slug:forum_name_slug>/post/')

        else:

            print(form.errors)

    return render(request, 'main/course/<slug:course_name_slug>/<slug:forum_name_slug>/post/', {'form': form})


@login_required
def create_upvote(request):

    upvote = None

    # If user upvotes question
    if request.method == 'POST':
        upvote = Upvote()
        upvote.question = request.question
        upvote.user = request.user

    return render(request, 'main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/question', {'upvote': upvote})


@login_required
def enroll_user(request):

    enroll = None

    # If user enrolls in course
    if request.method == 'POST':
        enroll = Enrollment()
        enroll.course = request.course
        enroll.user = request.user

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

@login_required
def set_role(request):
    return render(request, 'main/request_sent.html')

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

    
    