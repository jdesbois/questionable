from django import forms
from main.models import Course, Lecture, Question, Reply


class CourseForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the course name")

    class Meta:
        model = Course
        fields = 'name'


class LectureFrom(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter lecture name")

    class Meta:
        model = Lecture
        exclude = 'course'


class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    question = forms.CharField(max_length=512)
    upvotes = forms.IntegerField(default=0)

    class Meta:
        model = Question
        exclude = 'lecture'


class ReplyForm(forms.ModelForm):
    reply = forms.CharField(max_length=512)

    class Meta:
        model = Reply
        exclude = 'question'
