import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'questionable.settings')

import django
django.setup()

from main.models import Lecture, Question


def populate():

    programming_questions = [
        {'title': 'Help, I\'ve deleted my path variable.',
         'question': 'Where can I buy a new laptop?'},
        {'title': 'What is MVC?',
        'question': 'Unsure how to implement model, view controller.'}
    ]

    databases_questions = [
        {'title': 'My database is odd',
         'question': 'How can I normalize it?'},
        {'title': 'SQL vs NoSQL',
         'question': 'What is the difference between SQL and NoSQL?'}
    ]

    lectures = {'Programming': {'questions': programming_questions},
                'Databases': {'questions': databases_questions}}


    for lect, lect_data in lectures.items():
        l = add_lecture(lect)
        for q in lect_data['questions']:
            add_question(l, q['title'], q['question'])

    # print lectures
    for l in Lecture.objects.all():
        for q in Question.objects.filter(lecture=l):
            print(f'- {l}: {q}')

def add_question(lect, title, question, upvotes=0):
    q = Question.objects.get_or_create(lecture=lect, title=title)[0]
    q.question = question
    q.upvotes = upvotes
    q.save()
    return q


def add_lecture(name):
    l = Lecture.objects.get_or_create(name=name)[0]
    l.save()
    return l


if __name__ == '__main__':
    print('Starting population script...')
    populate()
