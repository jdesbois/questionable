from django.test import TestCase
from main.models import Course

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
