from django.db import models


class Lecture(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    question = models.CharField(max_length=512)
    upvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.title