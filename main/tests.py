from django.test import TestCase
from main.models import Course, Lecture

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

    def test_crouse_lecture(self):
        lecture = Lecture.objects.get(name="Hello World")
        self.assertEquals(lecture.name, "Hello World")
        self.assertEquals(lecture.course.name, "Programming")