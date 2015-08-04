from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class TestCase(models.Model):
    test_name = models.CharField(max_length = 50)
    theme_name = models.ForeignKey(Theme)
    def __str__(self):
        return self.test_name

class Question(models.Model):
    test_name = models.ForeignKey(TestCase)
    name = models.CharField(max_length = 200)
    def __str__(self):
        return self.name

class Answer(models.Model):
    name = models.CharField(max_length=50)
    question = models.ForeignKey(Question)
    isRight = models.BooleanField()
    def __str__(self):
        return self.name
# Create your models here.
