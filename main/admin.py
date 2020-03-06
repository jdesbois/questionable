from django.contrib import admin
from main.models import Course, Lecture, Question, Reply

admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(Question)
admin.site.register(Reply)