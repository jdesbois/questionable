from django import forms
from main.models import Course, Lecture, Question, Reply, Comment, Profile
from django.contrib.auth.models import User



# Creates a from for a course tuple to add to database
class CourseForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter the course name")

    class Meta:
        model = Course
        fields = ('name',)


# Creates a form for a Lecture tuple to add to database
class LectureForm(forms.ModelForm):
    name = forms.CharField(max_length=128,
                           help_text="Please enter lecture name")

    class Meta:
        model = Lecture
        exclude = ('course',)


# Creates a form for a Lecture tuple to add to database
class QuestionForm(forms.ModelForm):
    title = forms.CharField(max_length=128)
    question = forms.CharField(max_length=512)

    class Meta:
        model = Question
        exclude = ('lecture',)


# Creates a form for a Lecture tuple to add to database
class ReplyForm(forms.ModelForm):
    reply = forms.CharField(max_length=512)

    class Meta:
        model = Reply
        exclude = ('question', 'user',)


# Creates a form for a Lecture tuple to add to database
class CommentForm(forms.ModelForm):
    comment = forms.CharField(max_length=512)

    class Meta:
        model = Comment
        exclude = ('question', 'user',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'picture',)
