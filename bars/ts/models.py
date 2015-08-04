from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Question(models.Model):
    theme_name = models.ForeignKey(Theme)
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
