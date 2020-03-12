from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    user = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    # why doesn't this work without setting default?
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Question(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=128)
    question = models.CharField(max_length=512)

    def __str__(self):
        return self.title


class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reply = models.CharField(max_length=512)
    user = models.ForeignKey(Tutor, on_delete=models.CASCADE, default=None)

    def __str__(self):
        # identify by primary key
        return "Reply: " + str(self.pk)


class Forum(models.Model):
    # why doesn't this work without setting default?
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=128)
    post = models.CharField(max_length=512)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    comment = models.CharField(max_length=512)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)

    def __str__(self):
        # identify by primary key
        return "Reply: " + str(self.pk)


class Upvote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "Upvote: " + str(self.pk)


class Enrollment(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, default=None)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return "Enrollment: " + str(self.pk)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=512)
    picture = models.ImageField(upload_to='static/images/', default='default.jpg')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
