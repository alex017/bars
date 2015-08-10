from django.db import models
from django.contrib.auth.models import User


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

class UserTestCaseAnswer(models.Model):
    user = models.ForeignKey(User)
    test_case_name = models.ForeignKey(TestCase)
#    isFinished = models.BooleanField(default = False)

    def __str__(self):
        return 'user = %s, testcase = %s' % (self.user, self.test_case_name)
    
class UserAnswer(models.Model):
    user_answer = models.ForeignKey(Answer)
    user_test_case_answer = models.ForeignKey(UserTestCaseAnswer)

class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

class TestQuestions(models.Model):
    user_test_case_answer = models.ForeignKey(UserTestCaseAnswer)
    questions = ListField()

    def __str__(self):
        return str(self.questions)

# Create your models here.
