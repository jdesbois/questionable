from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)

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
    title = models.CharField(max_length=128)
    question = models.CharField(max_length=512)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Reply(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reply = models.CharField(max_length=512)

    def __str__(self):
        # identify by primary key
        return "Reply: " + self.pk
