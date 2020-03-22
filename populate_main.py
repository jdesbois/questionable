import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionable.settings')

import django
django.setup()

from main.models import Course, Lecture, Question, Reply, Forum, Post, Comment, Tutor, Student, Upvote
from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model



def populate():
    ##############
    # Groups
    ##############
    lecturer = Group(name="Lecturer")
    # lecturer = Group.objects.create(name='Lecturer')
    lecturer.save()
    student = Group(name="Student")
    # student = Group.objects.create(name='Student')
    student.save()
    # extract perms of model object and adds it to specified group
    lecture_perms = ContentType.objects.get(app_label='main', model='lecture')
    l_perms = Permission.objects.filter(content_type=lecture_perms)

    reply_perms = ContentType.objects.get(app_label='main', model='reply')
    r_perms = Permission.objects.filter(content_type=reply_perms)

    comment_perms = ContentType.objects.get(app_label='main', model='comment')
    com_perms = Permission.objects.filter(content_type=comment_perms)

    course_perms = ContentType.objects.get(app_label='main', model='course')
    c_perms = Permission.objects.filter(content_type=course_perms)

    forum_perms = ContentType.objects.get(app_label='main', model='forum')
    f_perms = Permission.objects.filter(content_type=forum_perms)

    for x in l_perms:
        lecturer.permissions.add(x)
    for x in r_perms:
        lecturer.permissions.add(x)
    for x in com_perms:
        student.permissions.add(x)
    for x in c_perms:
        lecturer.permissions.add(x)
    for x in f_perms:
        lecturer.permissions.add(x)

    ##############
    # Users
    ##############

    # Default admin for /admin (REMOVE BEFORE DEPLOYING)
    admin = User.objects.create_user('admin', 'noreply@apple.com', 'HelloWorld123')
    User1 = get_user_model()
    user = User1.objects.get(username="admin")
    user.groups.remove(Group.objects.get(name="Student"))
    Student.objects.get(user=user).delete()
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()


    user1 = User.objects.create_user("John", "noreplay@apple.com", "johnpassword1")
    user2 = User.objects.create_user("Andrew", "noreplay@apple.com", "andrewpassword1")
    user3 = User.objects.create_user("Rebecca", "noreplay@apple.com", "rebeccapassword1")
    user4 = User.objects.create_user("Aaron", "noreplay@apple.com", "aaronpassword1")
    user5 = User.objects.create_user("Dave", "noreplay@apple.com", "davepassword1")
    user6 = User.objects.create_user("Claire", "noreplay@apple.com", "clairepassword1")
    user7 = User.objects.create_user("Becca", "noreplay@apple.com", "beccapassword1")
    user8 = User.objects.create_user("Alan", "noreplay@apple.com", "alanpassword1")
    user9 = User.objects.create_user("Archie", "noreplay@apple.com", "archiepassword1")
    user10 = User.objects.create_user("Steve", "noreplay@apple.com", "stevepassword1")
    user11 = User.objects.create_user("Dory", "noreplay@apple.com", "dorypassword1")
    user12 = User.objects.create_user("Mike", "noreplay@apple.com", "mikepassword1")
    user13 = User.objects.create_user("Indy", "noreplay@apple.com", "indypassword1")

    #Add student profile for student (which should be default) and add user to Student group
    student1 = add_student(user3)
    student2 = add_student(user4)
    student3 = add_student(user5)
    student4 = add_student(user6)
    student5 = add_student(user7)
    student6 = add_student(user8)
    student7 = add_student(user9)
    student8 = add_student(user10)
    student9 = add_student(user11)
    user3.groups.add(student)
    user4.groups.add(student)
    user5.groups.add(student)
    user6.groups.add(student)
    user7.groups.add(student)
    user8.groups.add(student)
    user9.groups.add(student)
    user10.groups.add(student)
    user11.groups.add(student)

    #Add tutors profile to user and add user to the Lecturer group
    tutor1 = add_tutor(user1)
    tutor2 = add_tutor(user2)
    tutor3 = add_tutor(user12)
    tutor4 = add_tutor(user13)
    user1.groups.add(lecturer)
    user2.groups.add(lecturer)
    user12.groups.add(lecturer)
    user13.groups.add(lecturer)

    ####################
    # Questions
    ####################

    hello_world_questions = [
        {'title': 'What version of Java are we using?',
         'question': "I've seen online that there are 13 versions of Java, which version will we use for this course?",
         'author': student1,
         'upvotes': [student1],
         'replies': [["We will be using Java 1.8.", tutor1],
                     ["Also worth investigating Eclipse, the development environment the staff will use to teach.",
                      tutor1]]},
        {'title': 'Main method help.',
         'question': 'What is the correct way to write a main metho?',
         'author': student2,
         'upvotes': [student2],
         'replies': [["public static void main(String args){}", tutor1],
                     ["Try inserting 'System.out.println(\"Hello World\");' in this method.", tutor1]]}
    ]

    intro_to_java_questions = []

    objects_questions = [
        {'title': 'Constructors',
         'question': 'How is a constructor created and used?',
         'author': student4,
         'upvotes': [student3, student4],
         'replies': [["A constructor is called to create an initial instance of an object." +
                      "It can be passed variables and use these to set the initial parameters of the object",
                      tutor2]]},
        {'title': 'Pass by reference',
         'question': 'What is the difference between pass by reference and by value?',
         'author': student3,
         'upvotes': [student4],
         'replies': [["When an object is passed by reference, the passed value is an address pointing to that object." +
                      "When an object is passed by value the object itself is passed", tutor2],
                     ["Note that objects can only be passed by reference in Java.", tutor2]]}
    ]

    DBIntro_questions = [
        {'title': 'What is a database',
         'question': 'And how does it work?',
         'author': student5,
         'upvotes': [student5, student6],
         'replies': []},
        {'title': 'What is a foreign key?',
         'question': 'Struggling to understand the difference between primary keys and foreign keys and the constraints on them.',
         'author': student6,
         'upvotes': [],
         'replies': []}
    ]

    ERDiagram_questions = [

    ]

    SQL_questions = [
        {'title': 'My database is odd',
         'question': 'How can I normalize it?',
         'author': student7,
         'upvotes': [student8],
         'replies': []},
        {'title': 'SQL vs NoSQL',
         'question': 'What is the difference between SQL and NoSQL?',
         'author': student8,
         'upvotes': [student7],
         'replies': []}
    ]

    itech_intro_questions = [
        {'title': 'New to Python',
         'question': "I've never programmed in python before. Where can I find good resources to learn?",
         'author': student9,
         'upvotes': [],
         'replies': [["The course textbook 'Tango with Django' provides a list of resource.", tutor3],
                     ["I personally would recommend CodeAcademy.com", tutor3]]},
        {'title': 'Lab grading',
         'question': 'How will labs be marked?',
         'author': student5,
         'upvotes': [student6, student4],
         'replies': [["The chapters in TWD have automated tests, we will check your code against these.", tutor3]]}
    ]

    django_questions = [
        {'title': 'Versioning',
         'question': 'What versions of python and django will we be using?',
         'author': student7,
         'upvotes': [student1],
         'replies': [["Python 3.7.5 & Django 2.1.5", tutor3]]},
        {'title': 'Virtual environment',
         'question': 'What is the best way to set up a virtual environment on windows',
         'author': student4,
         'upvotes': [student2],
         'replies': [["I would recommend Anaconda Prompt, but the IDE pycharm also offers virtual environment options", tutor3]]}
    ]

    html_questions = []

    ads_intro_questions = [
        {'title': 'Labs Assessment',
         'question': 'Will the labs form part of our assessment?',
         'author': student6,
         'upvotes': [student5, student4],
        'replies': [["No, however we will help students with their assessed exercises at the lab", tutor4]]},
        {'title': 'Exam',
         'question': 'What format will the exam take?',
         'author': student9,
         'upvotes': [student8],
        'replies': [["The exam will be multiple choice.", tutor4]]}
    ]

    algorithms_questions = []

    linked_lists_questions = []

    ai_intro_questions = []

    intro_to_data_modeling_questions = [{'title': 'Use of alternative database software',
         'question': 'Can we use MYSQL instead of PgAdmin?',
         'author': student6,
         'upvotes': [student5, student4],
        'replies': [["No, as the automiated tests require functionality that doesn\'t exist in MYSQL.", tutor4]]},
        {'title': 'Issue setting up modeling environment',
         'question': 'Is it possible to set aside lab time to help students set up their environments?',
         'author': student8,
         'upvotes': [student9],
        'replies': [["Yes of course! The first 20 minutes of next weeks labs will be used as a time to help students set everything up.", tutor4]]}]

    deep_learning_basics_questions = [{'title': 'Labs Assessment',
         'question': 'Will the labs form part of our assessment?',
         'author': student6,
         'upvotes': [student5, student4],
        'replies': [["Yes, the deep learning labs are graded and will contribute to your final mark.", tutor4]]},
        {'title': 'Meeting time',
         'question': 'Is it possible to set aside some meeting time so student can come and ask questions?',
         'author': student9,
         'upvotes': [student8],
        'replies': [["Unfortunately due to commitments with other courses I will not be able to set aside time for private meetings. I will be available in all labs to answer questions and I try to actively respond to emails", tutor4]]}]


    ################
    # Lectures
    ################

    programming_lectures = {'Hello World': {'questions': hello_world_questions},
                            'Intro to Java': {'questions': intro_to_java_questions},
                            'Objects': {'questions': objects_questions}}

    database_lectures = {'Intro to DB': {'questions': DBIntro_questions},
                         'ER Diagrams': {'questions': ERDiagram_questions},
                         'SQL': {'questions': SQL_questions}}

    internet_technology_lectures = {'ITech Intro': {'questions': itech_intro_questions},
                            'Django': {'questions': django_questions},
                            'HTML': {'questions': html_questions}}

    algorithms_lectures = {'ADS Intro': {'questions': ads_intro_questions},
                            'Algorithms': {'questions': algorithms_questions},
                            'Linked Lists': {'questions': linked_lists_questions}}

    artificial_intelligence_lectures = {'AI Intro': {'questions': ai_intro_questions},
                            'Intro to data modelling': {'questions': intro_to_data_modeling_questions},
                            'Deep learning basics': {'questions': deep_learning_basics_questions}}


    ####################
    # Posts (Forum)
    ####################

    programming_forum_posts = [
        {'title': 'Book for sale - Big Java Late Objects',
         'post': 'Book for sale, unused.',
         'author': user3,
         'comments': [["How much?", user4],
                      ["£10", user3],
                      ["Can I pick it up Friday?", user5]]},
        {'title': 'Group wanted.',
         'post': 'Looking for group members for project.',
         'author': user5,
         'comments': [["We need one more for our team if you'd like to join?", user3],
                      ["That would be great, thanks!", user4]]}
    ]

    database_forum_posts = [
        {'title': 'Anyone else having trouble with Postgres?',
         'post': 'Server won\'t run.',
         'author': user4,
         'comments': [["I did, I found the lecture video from 23/10 helpful.", user3],
                      ["There's a great page on stack overflow if you google 'Postgres setup for PGAdmin'", user5]]},
        {'title': 'Study buddies wanted - apply within.',
         'post': 'Looking for people to study databases with',
         'author': user3,
         'comments': [["We have a study group every Thursday at 7pm", user4],
                      ["We have a space in our study group! We meet after Itech every Wednesday!", user5]]}
    ]

    internet_technology_forum_posts = [
        {'title': 'Can anyone help me with rango chapter 6?',
         'post': 'I keep getting a page not found error but I made the template just as they said in the book?',
         'author': user5,
         'comments': [["I can help you out if you want to set up zoom and screenshare?", user3],
                      ["Do you have any screenshots? Or a link to your github?", user4]]},
        {'title': 'Need help setting up my virtual environment',
         'post': 'I don\'t understand what a virtual environment or how it helps to start with so I\'m totally lost',
         'author': user4,
         'comments': [["There's a page dedicated to this at the end of the book? Just check the contents page", user3],
                      ["Have you tried googling it?", user5]]}
    ]

    algorithms_forum_posts = [
        {'title': 'Does anyone have a good link to find some more material on complexity calculations?',
         'post': 'I\'ve went through all the lecture material and I still don\'t understand how to calculate a big O notation! Help please!!',
         'author': user3,
         'comments': [["Theres some great stuff on Geek for Geeks!", user5],
                      ["Yeah I found the Geek for Geek material really helpful too!", user4]]},
        {'title': 'Need help with lab 3',
         'post': 'For question 2 do I need to use the classes from last week?',
         'author': user4,
         'comments': [["I'm not sure either! I eamailed the lecturer about it and I'm waiting for a reply. Will let you know when they get back to me", user3],
                      ["The start of the lab says that the question require last weeks lab.", user5]]}
    ]

    artificial_intelligence_forum_posts = [
        {'title': 'I\'m getting an issue with my deep learning model, it keeps assigning the dataset backwards?',
         'post': 'Everything thats not a car is getting tagged with car and for some reason it thinks all cars are giraffes, help!',
         'author': user5,
         'comments': [["I can help you out if you want to set up skype and screenshare?", user3],
                      ["Can you link to your github so I can see if I can find an issue?", user4]]},
        {'title': 'I made a serious mistake',
         'post': 'I downloaded the wrong deeplearning package and now my model has taken over the trident program. What do I do?!',
         'author': user4,
         'comments': [["This might be a bit beyond a forum post?", user3],
                      ["Lol! You created skynet...", user5]]}
    ]

    ################
    # Forums
    ################

    programming_forum = {'Programming Forum': {'posts': programming_forum_posts}}

    database_forum = {'Database Forum': {'posts': database_forum_posts}}

    internet_technology_forum = {'Internet Technology': {'posts': internet_technology_forum_posts}}

    algorithms_forum = {'Algorithms': {'posts': algorithms_forum_posts}}

    artificial_intelligence_forum = {'Artificial Intelligence': {'posts': artificial_intelligence_forum_posts}}

    ##############
    # Courses
    ##############

    courses = {'Programming': {'lectures': programming_lectures,
                               'forum': programming_forum,
                               'bio': "The course aims to provide an initial introudction to programming using the programming language Java, giving a basic coverage of object oriented programming, data structure and algorithms."},
               'Databases': {'lectures': database_lectures,
                             'forum': database_forum,
                               'bio': "The course teaches students the fundamentals of database theory as well as applications. The focus is on relational databases. Student will learn to design normalized databases and implement them using SQL."},
               'Internet Technology': {'lectures': internet_technology_lectures,
                                       'forum': internet_technology_forum,
                                       'bio': "This course introduces students to web development using the python-base framework Django. Students will gain exposure to a wide range of technologies including; HTML, CSS, Javascript, Django, JQuery, AJAX and others."},
               'Algorithms': {'lectures': algorithms_lectures,
                              'forum': algorithms_forum,
                               'bio': "This course intends to develop students understanding of algorithms and data structures. Students will learn how to write algorithm and study their efficiency. The course also covers a range of abstract data types and how these can be implemented in data structures."},
               'Artificial Intelligence': {'lectures': artificial_intelligence_lectures,
                                           'forum': artificial_intelligence_forum,
                                           'bio': "This course introduces the concept of artificial intelligence using python machine learning models. Students will gain an understanding of basic machine learning modeling and how to expand multiple machine learning nodes into s deep learning AI."}}

    for course, course_data in courses.items():
        c = add_course(course, course_data['bio'])
        for lecture, lecture_data in course_data['lectures'].items():
            l = add_lecture(c, lecture)
            for question in lecture_data['questions']:
                q = add_question(l, question['title'], question['question'], question['author'])
                for voter in question['upvotes']:
                    add_upvote(q, voter)
                for reply in question['replies']:
                    add_reply(q, reply[0], reply[1])
        for forum, forum_data in course_data['forum'].items():
            f = add_forum(c, forum)
            for post in forum_data['posts']:
                p = add_post(f, post['title'], post['post'], post['author'])
                for comment in post['comments']:
                    add_comment(p, comment[0], comment[1])


def add_upvote(question, user):
    u = Upvote.objects.get_or_create(question=question, user=user)[0]
    u.save()
    return u


def add_reply(question, reply, user):
    r = Reply.objects.get_or_create(question=question, reply=reply)[0]
    r.user = user
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


def add_comment(post, comment, user):
    c = Comment.objects.get_or_create(post=post, comment=comment)[0]
    c.user = user
    c.save()
    return c


def add_post(forum, title, post, user):
    q = Post.objects.get_or_create(forum=forum, title=title)[0]
    q.post = post
    q.user = user
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
    student = Student.objects.get(user=user).delete()
    t = Tutor.objects.get_or_create(user=user)[0]
    t.save()
    return t

if __name__ == '__main__':
    print('Starting population script...')
    populate()
    print('Finished.')

