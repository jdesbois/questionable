from django.test import TestCase
from main.models import Course, Lecture, Question, Student, Tutor, Reply
from django.contrib.auth.models import User

# Create your tests here.
class CourseTestCase(TestCase):
    def setUp(self):
        Course.objects.create(name="Programming")
        Course.objects.create(name="Database")

    def test_course_name(self):
        course1 = Course.objects.get(name="Programming")
        course2 = Course.objects.get(name="Database")
        self.assertEquals(course1.name, "Programming")
        self.assertEquals(course2.name, "Database")

class LectureTestCase(TestCase):
    def setUp(self):
        course = Course.objects.create(name="Programming")
        Lecture.objects.create(name="Hello World", course=course)

    def test_lecture(self):
        lecture = Lecture.objects.get(name="Hello World")
        self.assertEquals(lecture.name, "Hello World")
        self.assertEquals(lecture.course.name, "Programming")

class QuestionTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="John", email="noreplay@apple.com", password="password123")
        student = Student.objects.create(user=user)
        course = Course.objects.create(name="Programming")
        lecture = Lecture.objects.create(name="Hello World", course=course)
        Question.objects.create(title="Help",question="deleted path variable help", lecture=lecture, user=student)
    
    def test_question(self):
        question = Question.objects.get(title="Help")
        self.assertEquals(question.title, "Help")
        self.assertEquals(question.lecture.name, "Hello World")
        self.assertEquals(question.lecture.course.name, "Programming")

class ReplyTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="John", email="noreplay@apple.com", password="password123")
        user2 = User.objects.create(username="Dory", email="noreplay@apple.com", password="password123")
        student = Student.objects.create(user=user1)
        tutor = Tutor.objects.create(user=user2)
        course = Course.objects.create(name="Programming")
        lecture = Lecture.objects.create(name="Hello World", course=course)
        question = Question.objects.create(title="Help",question="deleted path variable help", lecture=lecture, user=student)
        Reply.objects.create(reply="you stupid", user=tutor, question= question)

    def test_reply(self):
        reply = Reply.objects.get(reply="you stupid")
        self.assertEquals(reply.reply, "you stupid")
        self.assertEquals(reply.question.title, "Help")
        self.assertEquals(reply.user.user.username, "Dory")
