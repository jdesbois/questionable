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

    users = [
        {
            'username': 'Dory',
            'email': 'noreply@apple.com',
            'password': 'dorypassword1',
        },
        {
            'username': 'Mike',
            'email': 'noreply@apple.com',
            'password': 'mikepassword1',
        },
        {
            'username': 'Becca',
            'email': 'noreply@apple.com',
            'password': 'beccapassword1',
        },
        {
            'username': 'Archie',
            'email': 'noreply@apple.com',
            'password': 'archiepassword1',
        },
        {
            'username': 'Alan',
            'email': 'noreply@apple.com',
            'password': 'alanpassword1',
        },
        {
            'username': 'Claire',
            'email': 'noreply@apple.com',
            'password': 'clairepassword1',
        },
        {
            'username': 'Dave',
            'email': 'noreply@apple.com',
            'password': 'davepassword1',
        },
        {
            'username': 'Indy',
            'email': 'indy@carrot.com',
            'password': 'ILoveCarrots',
        },
    ]

    for user in users:
        u = User.objects.create_user(user['username'], user['email'], user['password'])
        add_student(u)

    # Default admin for /admin (REMOVE BEFORE DEPLOYING)
    admin = User.objects.create_user('admin', 'noreply@apple.com', 'HelloWorld123')
    User1 = get_user_model()
    user = User1.objects.get(username="admin")
    user.is_staff = True
    user.is_admin = True
    user.is_superuser = True
    user.save()

    user1 = User.objects.create_user("John", "noreplay@apple.com", "johnpassword1")
    user2 = User.objects.create_user("Andrew", "noreplay@apple.com", "andrewpassword1")
    user3 = User.objects.create_user("Rebecca", "noreplay@apple.com", "rebeccapassword1")
    user4 = User.objects.create_user("Aaron", "noreplay@apple.com", "aaronpassword1")
    user5 = User.objects.create_user("Bob", "noreplay@apple.com", "bobpassword1")

    student3 = add_student(user3)
    student4 = add_student(user4)

    user4.groups.add(student)
    user3.groups.add(student)
    tutor1 = add_tutor(user1)
    tutor2 = add_tutor(user2)

    user1.groups.add(lecturer)
    user2.groups.add(lecturer)

    ####################
    # Questions
    ####################

    hello_world_questions = [
        {'title': 'What version of Java are we using?',
         'question': "I've seen online that there are 13 versions of Java, which version will we use for this course?",
         'author': student3,
         'replies': [["We will be using Java 1.8.", tutor1],
                     ["Also worth investigating Eclipse, the development environment the staff will use to teach.",
                      tutor1]]},
        {'title': 'Main method help.',
         'question': 'What is the correct way to write a main metho?',
         'author': student4,
         'replies': [["public static void main(String args){}", tutor1],
                     ["Try inserting 'System.out.println(\"Hello World\");' in this method.", tutor1]]}
    ]

    intro_to_java_questions = []

    objects_questions = [
        {'title': 'Constructors',
         'question': 'How is a constructor created and used?',
         'author': student4,
         'replies': [["A constructor is called to create an initial instance of an object." +
                      "It can be passed variables and use these to set the initial parameters of the object",
                      tutor2]]},
        {'title': 'Pass by reference',
         'question': 'What is the difference between pass by reference and by value?',
         'author': student3,
         'replies': [["When an object is passed by reference, the passed value is an address pointing to that object." +
                      "When an object is passed by value the object itself is passed", tutor2],
                     ["Note that objects can only be passed by reference in Java.", tutor2]]}
    ]

    DBIntro_questions = [
        {'title': 'What is a database',
         'question': 'And how does it work?',
         'author': student4,
         'replies': []},
        {'title': 'What is a foreign key?',
         'question': 'And where is it from?',
         'author': student3,
         'replies': []}
    ]

    ERDiagram_questions = [

    ]

    SQL_questions = [
        {'title': 'My database is odd',
         'question': 'How can I normalize it?',
         'author': student3,
         'replies': []},
        {'title': 'SQL vs NoSQL',
         'question': 'What is the difference between SQL and NoSQL?',
         'author': student4,
         'replies': []}
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

    internet_technology_lectures = {}

    algorithms_lectures = {}

    artificial_intelligence_lectures = {}


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
                      ["Do you have any screenshots? Or a link to your github?", user4]]}
        {'title': 'Need help setting up my virtual environment',
         'post': 'I don\'t understand what a virtual environment or how it helps to start with so I\'m totally lost',
         'author': user4,
         'comments': [["There's a page dedicated to this at the end of the book? Just check the contents page", user3],
                      ["Have you tried googling it?", user5]]}
    ]

    algorithms_forum_posts = [
        {'title': 'Does anyone have a good link to find some more material on complexity calculations?',
         'post': 'I\'ve went through all the lecture material and I still don\'t understand how to calculate a big O notation! Help please!!',
         'author': user5,
         'comments': [["Theres some great stuff on Geek for Geeks!", user3],
                      ["Yeah I found the Geek for Geek material really helpful too!", user4]]}
        {'title': 'Need help with lab 3',
         'post': 'For question 2 do I need to use the classes from last week?',
         'author': user4,
         'comments': [["I'm not sure either! I eamailed the lecturer about it and I'm waiting for a reply. Will let you know when they get back to me", user3],
                      ["The start of the lab says that the question require last weeks lab.", user5]]}
    ]

    artificial_intelligence_forum_posts = [
        {'title': 'Can anyone help me with rango chapter 6?',
         'post': 'I keep getting a page not found error but I made the template just as they said in the book?',
         'author': user5,
         'comments': [["I can help you out if you want to set up zoom and screenshare?", user3],
                      ["Do you have any screenshots? Or a link to your github?", user4]]}
        {'title': 'Need help setting up my virtual environment',
         'post': 'I don\'t understand what a virtual environment or how it helps to start with so I\'m totally lost',
         'author': user4,
         'comments': [["There's a page dedicated to this at the end of the book? Just check the contents page", user3],
                      ["Have you tried googling it?", user5]]}
    ]

    ################
    # Forums
    ################

    programming_forum = {'Programming Forum': {'posts': programming_forum_posts}}

    database_forum = {'Database Forum': {'posts': database_forum_posts}}

    internet_technology_forum = {'Internet Technology': {'posts': internet_technology_forum_posts}}

    ##############
    # Courses
    ##############

    courses = {'Programming': {'lectures': programming_lectures, 'forum': programming_forum},
               'Databases': {'lectures': database_lectures, 'forum': database_forum},
               'Internet Technology': {'lectures': internet_technology_lectures, 'forum': internet_technology_forum},
               'Algorithms': {'lectures': algorithms_lectures, 'forum': algorithms_forum_posts},
               'Artificial Intelligence': artificial_intelligence_lectures, 'forum': artificial_intelligence_forum_posts}

    for course, course_data in courses.items():
        c = add_course(course, "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse laoreet consectetur odio ut fermentum. Mauris eleifend facilisis placerat. Praesent nec velit consequat, suscipit dui quis, maximus tellus. Donec volutpat consectetur ex a ultrices. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean ullamcorper tempus egestas. In auctor a risus consectetur cursus. Phasellus in sodales nibh. Duis finibus diam lectus, et pellentesque massa feugiat at. Donec molestie rutrum varius. In sollicitudin, massa id tristique rhoncus, odio risus consectetur quam, vel iaculis neque nisi non arcu. Suspendisse vulputate dolor nulla, vel tristique purus pretium ut. In hac habitasse.")
        for lecture, lecture_data in course_data['lectures'].items():
            l = add_lecture(c, lecture)
            for question in lecture_data['questions']:
                q = add_question(l, question['title'], question['question'], question['author'])
                for reply in question['replies']:
                    add_reply(q, reply[0], reply[1])
        for forum, forum_data in course_data['forum'].items():
            f = add_forum(c, forum)
            for post in forum_data['posts']:
                p = add_post(f, post['title'], post['post'], post['author'])
                for comment in post['comments']:
                    add_comment(p, comment[0], comment[1])


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
    t = Tutor.objects.get_or_create(user=user)[0]
    t.save()
    return t

if __name__ == '__main__':
    print('Starting population script...')
    populate()
    print('Finished.')

