from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# profile model to store additional user information

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # one to one relation with user table
    phone = models.CharField(max_length=10, default='')
    college = models.CharField(blank=True, max_length=255)
    totalScore = models.IntegerField(default=0)
    junior = models.BooleanField(default=True)
    correctly_answered = models.IntegerField(default=0)
    chances = models.IntegerField(default=3)
    latestSubTime = models.DateTimeField(
        auto_now=True)  # auto_now = True updates profile entry everytime you save a profile object

    def __str__(self):
        # displays username in list of objects in admin panel of django

        return self.user.username


# question model to store information regarding questions

class Question(models.Model):
    quesTitle = models.CharField(max_length=255)
    quesDesc = models.TextField(default="")
    sampleInput = models.TextField(default="")
    sampleOutput = models.TextField(default="")
    successfulAttempts = models.IntegerField(default=0)
    numberOfAttempts = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __str__(self):
        # displays question title in list of objects in admin panel of django

        return self.quesTitle


# submissions model to save information regarding user submissions

class Submissions(models.Model):
    languages = [('c', 'C'), ('cpp', 'C++'), ('py', 'Python')]

    # many to many relation between users and questions i.e. the number of submissions

    quesID = models.ForeignKey(Question, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)

    language = models.CharField(max_length=3, choices=languages)
    code = models.TextField(max_length=10000000, default="")
    attempt = models.IntegerField(default=0)
    status = models.CharField(default='NA', max_length=5)
    submission_time = models.CharField(default="", max_length=15)
    score = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)

    class Meta:
        # to display table name in accordance with grammar rules in admin panel

        verbose_name = 'Submissions'
        verbose_name_plural = 'Submissions'

    def __str__(self):
        # displays username and question number in list of objects in admin panel of django

        return self.userID.username + " - question-" + str(self.quesID.pk)
