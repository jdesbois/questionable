import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionable.settings')

import django
django.setup()

from main.models import Course, Lecture, Question, Reply, Forum, Post, Comment, Tutor, Student
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model



def populate():

    ####################
    # Questions
    ####################

    hello_world_questions = [
        {'title': 'Help, I\'ve deleted my path variable.',
         'question': 'Where can I buy a new laptop?'},
        {'title': 'What is MVC?',
        'question': 'Unsure how to implement model, view controller.'}
    ]

    intro_to_java_questions =[]

    objects_questions = [
        {'title': 'Constructors',
         'question': 'How is a constructor created and used?'},
        {'title': 'Pass by reference',
         'question': 'What is the difference between pass by reference and by value?'}
    ]

    DBIntro_questions = [
        {'title': 'What is a database',
         'question': 'And how does it work?'},
        {'title': 'What is a foreign key?',
         'question': 'And where is it from?'}
    ]

    ERDiagram_questions = [

    ]

    SQL_questions = [
        {'title': 'My database is odd',
         'question': 'How can I normalize it?'},
        {'title': 'SQL vs NoSQL',
         'question': 'What is the difference between SQL and NoSQL?'}
    ]

    ################
    # Lectures
    ################

    programming_lectures = {'Hello World': {'questions': hello_world_questions},
                            'Intro to Java': {'questions': intro_to_java_questions},
                            'Objects': {'questions': objects_questions}}

    database_lectures = {'Intro to DB': {'questions': DBIntro_questions},
                         'ER Diagrams': {'questions': ERDiagram_questions},
                         'SQL': {'questions': SQL_questions}}




    ####################
    # Posts (Forum)
    ####################

    programming_forum_posts = [
        {'title': 'Book for sale - Big Java Late Objects',
            'post': 'Book for sale, unused.'},
        {'title': 'Group wanted.',
            'post': 'Looking for group members for project.'}
    ]

    database_forum_posts = [
        {'title': 'Anyone else having trouble with Postgres?',
         'post': 'Server won\'t run.'},
        {'title': 'Study buddies wanted - apply within.',
         'post': 'Looking for people to study databases with'}
    ]


    ################
    # Forums
    ################

    programming_forum = {'Porgramming Forum': {'posts': programming_forum_posts}}

    database_forum = {'Database Forum': {'posts': database_forum_posts}}

    ##############
    # Courses
    ##############

    courses = {'Programming': {'lectures': programming_lectures, 'forum': programming_forum},
               'Databases': {'lectures': database_lectures, 'forum': database_forum}}

    ##############
    # Groups
    ##############
    lecturer = Group(name="Lecturer")
    # lecturer = Group.objects.create(name='Lecturer')
    lecturer.save()
    student = Group(name="Student")
    # student = Group.objects.create(name='Student')
    student.save()

    
    content_type = ContentType.objects.get(app_label='main', model='lecture')

    perms = Permission.objects.filter(content_type=content_type)
    
    for x in perms:
        lecturer.permissions.add(x)
    
   

    ##############
    # Users
    ##############
    user1 =  User.objects.create_user('John', 'noreply@apple.com', 'johnpassword1')
    user2 = User.objects.create_user('Andrew', 'noreply@apple.com', 'andrewpassword1')
    user3 = User.objects.create_user('Rebecca', 'noreply@apple.com', 'rebeccapassword1')
    user4 = User.objects.create_user('Aaron', 'noreply@apple.com', 'aaronpassword1')

    user1.groups.add(lecturer)
    user2.groups.add(lecturer)
    user3.groups.add(student)
    user4.groups.add(student)
  

    # Default admin for /admin (REMOVE BEFORE DEPLOYING)
    admin = User.objects.create_user('admin', 'noreply@apple.com','HelloWorld123')
    User1 = get_user_model()
    user = User1.objects.get(username="admin")
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()


    student3 = add_student(user3)
    student4 = add_student(user4)
    tutor1 = add_tutor(user1)
    tutor2 = add_tutor(user2)

    for course, course_data in courses.items():
        c = add_course(course, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse laoreet consectetur odio ut fermentum. Mauris eleifend facilisis placerat. Praesent nec velit consequat, suscipit dui quis, maximus tellus. Donec volutpat consectetur ex a ultrices. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean ullamcorper tempus egestas. In auctor a risus consectetur cursus. Phasellus in sodales nibh. Duis finibus diam lectus, et pellentesque massa feugiat at. Donec molestie rutrum varius. In sollicitudin, massa id tristique rhoncus, odio risus consectetur quam, vel iaculis neque nisi non arcu. Suspendisse vulputate dolor nulla, vel tristique purus pretium ut. In hac habitasse.")
        for lecture, lecture_data in course_data['lectures'].items():
            l = add_lecture(c, lecture)
            for question in lecture_data['questions']:
                q = add_question(l, question['title'], question['question'], student4)
                add_reply(q, "Donec aliquam dolor sapien, sagittis posuere dolor molestie vel. Aliquam arcu orci, luctus id vestibulum eget, dignissim egestas leo. Vivamus bibendum augue augue, a gravida ante condimentum id. Quisque ut rhoncus nulla. Ut eleifend est ut dui ultrices interdum. Quisque nec vulputate felis. Ut non tortor turpis. Vestibulum pretium nec erat vitae finibus. Maecenas consequat est sit amet fringilla fermentum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae;")
        for forum, forum_data in course_data['forum'].items():
            f = add_forum(c, forum)
            for post in forum_data['posts']:
                c = add_post(f, post['title'], post['post'])
                # add_reply(question, "Test reply text")


def add_reply(question, reply):
    r = Reply.objects.get_or_create(question=question, reply=reply)[0]
    r.save()
    return r


def add_question(lect, title, question, user):
    q = Question.objects.get_or_create(lecture=lect, title=title)[0]
    q.question = question
    q.user = user
    q.save()
    return q


def add_lecture(course, name):
    l = Lecture.objects.get_or_create(course=course, name=name)[0]
    l.save()
    return l


def add_comment(post, comment):
    c = Comment.objects.get_or_create(post=post, comment=comment)[0]
    c.save()
    return c


def add_post(forum, title, post):
    q = Post.objects.get_or_create(forum=forum, title=title)[0]
    q.question = post
    q.save()
    return q


def add_forum(course, name):
    f = Forum.objects.get_or_create(course=course, name=name)[0]
    f.save()
    return f


def add_course(name, bio):
    c = Course.objects.get_or_create(name=name, bio=bio)[0]
    c.save()
    return c

def add_student(user):
    s = Student.objects.get_or_create(user=user)[0]
    s.save()
    return s

def add_tutor(user):
    t = Tutor.objects.get_or_create(user=user)[0]
    t.save()
    return t


if __name__ == '__main__':
    print('Starting population script...')
    populate()
    print('Finished.')

