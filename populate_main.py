import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionable.settings')

import django
django.setup()

from main.models import Course, Lecture, Question, Reply, Tutor, Student
from django.db import models
from django.contrib.auth.models import User


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


    ##############
    # Courses
    ##############

    courses = {'Programming': {'lectures': programming_lectures},
               'Databases': {'lectures': database_lectures}}

    ##############
    # Users
    ##############
    user1 =  User.objects.create_user('John', 'noreply@apple.com', 'johnpassword1')
    user2 = User.objects.create_user('Andrew', 'noreply@apple.com', 'andrewpassword1')
    user3 = User.objects.create_user('Rebecca', 'noreply@apple.com', 'rebeccapassword1')
    user4 = User.objects.create_user('Aaron', 'noreply@apple.com', 'aaronpassword1')

    add_student(user1)
    add_student(user2)
    add_tutor(user3)
    add_tutor(user4)

    for course, course_data in courses.items():
        c = add_course(course)
        for lecture, lecture_data in course_data['lectures'].items():
            l = add_lecture(c, lecture)
            for question in lecture_data['questions']:
                q = add_question(l, question['title'], question['question'])
                # add_reply(question, "Test reply text")


def add_reply(question, reply):
    r = Reply.objects.get_or_create(question=question, reply=reply)[0]
    r.save()
    return r


def add_question(lect, title, question, upvotes=0):
    q = Question.objects.get_or_create(lecture=lect, title=title)[0]
    q.question = question
    q.upvotes = upvotes
    q.save()
    return q


def add_lecture(course, name):
    l = Lecture.objects.get_or_create(course=course, name=name)[0]
    l.save()
    return l

def add_course(name):
    c = Course.objects.get_or_create(name=name)[0]
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

