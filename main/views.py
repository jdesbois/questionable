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
from django.db.models import Count


# DISPLAY VIEWS


@login_required
def home(request):
    return render(request, 'core/home.html')


def index(request):
    upvotes = Upvote.objects.values('question').annotate(upvote_count=Count('question'))
    question_new = Question.objects.order_by('-id')[:3]
    questions_top = upvotes.order_by('-upvote_count')[:3]
    questions = Question.objects.filter(id__in=(questions_top[0]['question'],questions_top[1]['question'],questions_top[2]['question']))
    question = Question.objects.get(id=questions_top[0]['question'])
    

    context_dict = {}
    context_dict['questions'] = questions
    context_dict['newquestions'] = question_new

    return render(request, 'main/index.html', context=context_dict)


def show_courses(request):
    context_dict = {}
    course = {}
    current_user = request.user
    role = None

    if check_user(current_user) == 1:
        role = "student"
    elif check_user(current_user) == 2:
        role = "lecturer"
    else:
        role = None

    context_dict['role'] = role

    try:
        courses = Course.objects.all()
        context_dict['courses'] = courses

    except Course.DoesNotExist:
        context_dict['courses'] = None

    return render(request, 'main/courses.html', context=context_dict)


def show_course(request, course_name_slug):
    context_dict = {}

    current_user = request.user
    role = None

    if check_user(current_user) == 1:
        role = "student"
    elif check_user(current_user) == 2:
        role = "lecturer"
    else:
        role = None

    context_dict['role'] = role
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
        question_form = QuestionForm()
        reply_form = ReplyForm()

        reply_dict = {}
        upvote_dict = {}
        hasvoted_dict = {}

        current_user = request.user
        if check_user(current_user=current_user) == 2:
            is_tutor = True
            is_student = False
            print("tutor")
        elif check_user(current_user=current_user) == 1:
            is_student = True
            is_tutor = False
            print("student")
        else:
            is_student = False
            is_tutor = False
            print("neither")

        for question in question_list:
            reply_dict[question.title] = Reply.objects.filter(question=question)
            upvotes = Upvote.objects.filter(question=question)
            upvote_dict[question.title] = upvotes.count()

            if is_student:
                current_student = Student.objects.get(user=current_user)
                user_upvote = Upvote.objects.filter(question=question, user=current_student)

                if user_upvote.exists():
                    hasvoted_dict[question.title] = True
                else:
                    hasvoted_dict[question.title] = False

            # disable otherwise
            else:
                hasvoted_dict[question.title] = True

        context_dict['course'] = course
        context_dict['lecture'] = lecture
        context_dict['questions'] = question_list
        context_dict['reply_dict'] = reply_dict
        context_dict['upvote_dict'] = upvote_dict
        context_dict['hasvoted_dict'] = hasvoted_dict
        context_dict['question_form'] = question_form
        context_dict['reply_form'] = reply_form
        context_dict['is_tutor'] = is_tutor
        context_dict['is_student'] = is_student

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

    return render(request, 'main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/question.html',
                  context=context_dict)


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


def show_forum(request, course_name_slug, forum_name_slug):
    context_dict = {}

    try:
        course = Course.objects.get(slug=course_name_slug)
        forum = Forum.objects.get(slug=forum_name_slug)
        post_list = Post.objects.filter(forum=forum)
        post_form = PostForm()
        comment_form = CommentForm()

        comment_dict = {}

        current_user = request.user
        registered_account = check_user(current_user=current_user)

        if registered_account != 1 and registered_account != 2:
            is_user = False
        else:
            is_user = True

        if check_user(current_user=current_user) == 2:
            is_tutor = True
            print("tutor")
        else:
            is_tutor = False
            print("student")

        for post in post_list:
            comment_dict[post.title] = Comment.objects.filter(post=post)

        context_dict['course'] = course
        context_dict['forum'] = forum
        context_dict['posts'] = post_list
        context_dict['comment_dict'] = comment_dict
        context_dict['post_form'] = post_form
        context_dict['comment_form'] = comment_form
        context_dict['is_tutor'] = is_tutor
        context_dict['is_user'] = is_user

    except Forum.DoesNotExist:
        context_dict['forum'] = None
        context_dict['posts'] = None
        context_dict['comment_dict'] = None

    return render(request, 'main/forum.html', context=context_dict)


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
    questions = Question.objects.order_by('-id')[:3]
    posts = Post.objects.order_by('-id')[:3]
    replies = Reply.objects.all()[:3]
    context_dict['questions'] = questions
    context_dict['posts'] = posts
    context_dict['replies'] = replies

    if check_user(current_user) == 1:
        role = "Student"
    elif check_user(current_user) == 2:
        role = "Lecturer"
    else:
        role = None

    context_dict['role'] = role

    return render(request, 'main/profile.html', context=context_dict)




# CREATION VIEWS


@login_required
@permission_required('main.add_course', raise_exception=True)
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
@permission_required('main.add_lecture',  raise_exception=True)
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
        return redirect('/main/lecture/<slug:course_name_slug>/<slug:lecture_name_slug/')

    form = QuestionForm()

    current_user = request.user
    if check_user(current_user=current_user) == 2:
        is_tutor = True
        is_student = False
        print("tutor")
    elif check_user(current_user=current_user) == 1:
        is_student = True
        is_tutor = False
        print("student")
    else:
        is_student = False
        is_tutor = False
        print("neither")

    if is_student:
        current_student = Student.objects.get(user=current_user)
        # If user inputs comment
        if request.method == 'POST':
            print("after post")
            form = QuestionForm(request.POST)
            # If input is valid
            if form.is_valid():
                # Save the form
                question = form.save(commit=False)
                question.lecture = lecture
                question.user = current_student
                # first save creates id
                question.save()
                # re-save so slugify can pick up the question ID
                question.save()

                # return redirect('/main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/')
                return redirect(reverse('main:lecture',
                                        kwargs={'course_name_slug': course_name_slug,
                                                'lecture_name_slug': lecture_name_slug}))
            else:
                print(form.errors)
    else:
        return redirect(reverse('main:lecture',
                                kwargs={'course_name_slug': course_name_slug,
                                        'lecture_name_slug': lecture_name_slug}))

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

        current_user = request.user
        if check_user(current_user=current_user) == 2:
            is_tutor = True
            is_student = False
            print("tutor")
        elif check_user(current_user=current_user) == 1:
            is_student = True
            is_tutor = False
            print("student")
        else:
            is_student = False
            is_tutor = False
            print("neither")

        # create an upvote
        if is_student:
            current_student = Student.objects.get(user=current_user)
            u = Upvote.objects.get_or_create(question=question, user=current_student)

            # if a new object is created
            if (u[1] == True):
                u[0].save()
            # else, this upvote has already been cast
            else:
                print("Object already exists")

        # count upvotes for given question
        count = Upvote.objects.filter(question=question).count()

        # return updated count
        return HttpResponse(count)


@login_required
@permission_required('main.add_reply',  raise_exception=True)
def create_reply(request, course_name_slug, lecture_name_slug, question_name_slug):
    try:
        lecture = Lecture.objects.get(slug=lecture_name_slug)
    except Lecture.DoesNoExist:
        lecture = None

    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        course = None

    try:
        question = Question.objects.get(slug=question_name_slug)
    except Question.DoesNotExist:
        question = None

    if course is None or lecture is None:
        return redirect('/main/lecture/<slug:course_name_slug>/<slug:lecture_name_slug/')

    form = ReplyForm()

    current_user = request.user
    if check_user(current_user=current_user) == 2:
        is_tutor = True
        is_student = False
        print("tutor")
    elif check_user(current_user=current_user) == 1:
        is_student = True
        is_tutor = False
        print("student")
    else:
        is_student = False
        is_tutor = False
        print("neither")

    if is_tutor:
        current_tutor = Tutor.objects.get(user=current_user)
        # If user inputs comment
        if request.method == 'POST':
            form = ReplyForm(request.POST)
            # If input is valid
            if form.is_valid():
                # Save the form
                reply = form.save(commit=False)
                reply.user = current_tutor
                reply.question = question
                reply.save()
                return redirect(reverse('main:lecture',
                                        kwargs={'course_name_slug': course_name_slug,
                                                'lecture_name_slug': lecture_name_slug}))

            else:

                print(form.errors)

    return redirect(reverse('main:lecture',
                            kwargs={'course_name_slug': course_name_slug,
                                    'lecture_name_slug': lecture_name_slug}))


@login_required
@permission_required('main.add_forum',  raise_exception=True)
def create_forum(request, course_name_slug):
    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNoteExist:
        course = None
    if course is None:
        return redirect('main/forum/<slug:course_name_slug>')

    form = ForumForm()

    # If user inputs comment
    if request.method == 'POST':
        form = ForumForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            forum = form.save(commit=False)
            forum.course = course
            try: 
                forum.save()
            except:
                return redirect(reverse('main:error'))

            return redirect(reverse('main:course', kwargs={'course_name_slug': course_name_slug}))

        else:

            print(form.errors)

    context_dict = {'form': form, 'course': course}
    return render(request, 'main/create_forum.html', context_dict)


@login_required
def create_post(request, course_name_slug, forum_name_slug):
    # find lecture object
    try:
        forum = Forum.objects.get(slug=forum_name_slug)
    except Forum.DoesNoExist:
        forum = None

    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        course = None

    if course is None or forum is None:
        return redirect('/main/forum/<slug:course_name_slug>/<slug:forum_name_slug/')

    form = PostForm()

    if request.method == 'POST':
        print("after post")
        form = PostForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            post = form.save(commit=False)
            post.forum = forum
            post.user = request.user
            # save 1 creates id
            post.save()
            # save 2 uodates slug
            post.save()

            # return redirect('/main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/')
            return redirect(reverse('main:forum',
                                    kwargs={'course_name_slug': course_name_slug,
                                            'forum_name_slug': forum_name_slug}))
        else:
            print(form.errors)

    # return render(request, 'main/course/<slug:course_name_slug>/<slug:lecture_name_slug>/', {'form': form})
    return redirect(reverse('main:forum',
                            kwargs={'course_name_slug': course_name_slug,
                                    'forum_name_slug': forum_name_slug}))


@login_required
def create_comment(request, course_name_slug, forum_name_slug, post_name_slug):
    try:
        forum = Forum.objects.get(slug=forum_name_slug)
    except Forum.DoesNoExist:
        forum = None

    try:
        course = Course.objects.get(slug=course_name_slug)
    except Course.DoesNotExist:
        course = None

    try:
        post = Post.objects.get(slug=post_name_slug)
    except Post.DoesNotExist:
        post = None

    if course is None or forum is None or post is None:
        return redirect('/main/forum/<slug:course_name_slug>/<slug:forum_name_slug/')

    form = ReplyForm()

    # If user inputs comment
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # If input is valid
        if form.is_valid():
            # Save the form
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect(reverse('main:forum',
                                    kwargs={'course_name_slug': course_name_slug,
                                            'forum_name_slug': forum_name_slug}))

        else:

            print(form.errors)

    return redirect(reverse('main:forum',
                            kwargs={'course_name_slug': course_name_slug,
                                    'forum_name_slug': forum_name_slug}))


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
    context_dict = {}
    users = Student.objects.all()
    context_dict['users'] = users

    if request.method == 'POST':
        print(request.POST.get('selected_user'))
        selected_user = request.POST.get('selected_user')
        current_user = User.objects.get(username=selected_user)
        Tutor.objects.create(user=current_user)
        Student.objects.get(user=current_user).delete()
        
        student_group = Group.objects.get(name="Student")
        lecturer_group = Group.objects.get(name="Lecturer")
        current_user.groups.remove(student_group)
        current_user.groups.add(lecturer_group)
    else:


        return render(request, 'main/manage_users.html', context=context_dict)

    return render(request, 'main/manage_users.html', context=context_dict)

def delete_user(request):
    current_user = request.user
    current_user.delete()

    return render(request, 'main/delete_user.html')


def error(request):
    return render(request, 'main/error.html')


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
