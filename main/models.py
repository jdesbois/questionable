from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
# Signal makes sure that every user created is a Student    
@receiver(post_save, sender=User)
def create_or_update_student(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    bio = models.CharField(max_length=1024, null=True, blank=True, default=None)
    user = models.ForeignKey(Tutor, on_delete=models.CASCADE, null=True, blank=True, default=None)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    # why doesn't this work without setting default?
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Lecture, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Question(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    title = models.CharField(max_length=128)
    question = models.CharField(max_length=512)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = self.id
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reply = models.CharField(max_length=512)
    user = models.ForeignKey(Tutor, on_delete=models.SET_NULL, default=None, null=True)

    def __str__(self):
        # identify by primary key
        return "Reply: " + str(self.pk)


class Forum(models.Model):
    # why doesn't this work without setting default?
    course = models.ForeignKey(Course, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Forum, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    title = models.CharField(max_length=128)
    post = models.CharField(max_length=512)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = self.id
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    comment = models.CharField(max_length=512)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        # identify by primary key
        return "Reply: " + str(self.pk)


class Upvote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(Student, on_delete=models.SET_NULL, default=None, null=True, blank=True)

    def __str__(self):
        return "Upvote: " + str(self.pk)


#User Profile that has a one to one field with User. This is to expand the user model built into Django
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=512, default="Tell us a little about yourself....")
    picture = models.ImageField(upload_to='images/', default="images/default.jpg")

    def __str__(self):
        return self.user.username
#Receiver signal that insures that every user created has an associated Profile
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()