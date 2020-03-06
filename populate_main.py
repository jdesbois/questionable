import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionable.settings')

import django
django.setup()

from main.models import Course, Lecture, Question, Reply


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

    # lectures = {'Programming': {'questions': programming_questions},
    #             'Databases': {'questions': databases_questions}}





    for course, course_data in courses.items():
        c = add_course(course)
        for lecture, lecture_data in course_data['lectures'].items():
            l = add_lecture(c, lecture)
            for question in lecture_data['questions']:
                q = add_question(l, question['title'], question['question'])
                # add_reply(question, "Test reply text")


    # for lect, lect_data in lectures.items():
    #     l = add_lecture(lect)
    #     for q in lect_data['questions']:
    #         add_question(l, q['title'], q['question'])

    # # print lectures
    # for l in Lecture.objects.all():
    #     for q in Question.objects.filter(lecture=l):
    #         print(f'- {l}: {q}')


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


if __name__ == '__main__':
    print('Starting population script...')
    populate()


    # programming_questions = [
    #     {'title': 'Help, I\'ve deleted my path variable.',
    #      'question': 'Where can I buy a new laptop?'},
    #     {'title': 'What is MVC?',
    #     'question': 'Unsure how to implement model, view controller.'}
    # ]

    # databases_questions = [
    #     {'title': 'My database is odd',
    #      'question': 'How can I normalize it?'},
    #     {'title': 'SQL vs NoSQL',
    #      'question': 'What is the difference between SQL and NoSQL?'}
    # ]