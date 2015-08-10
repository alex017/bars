from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.views import logout
from .models import Theme, Question, Answer, TestCase, UserTestCaseAnswer, UserAnswer, TestQuestions
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

import json

class IndexView(generic.TemplateView):
    def get(self, request):
        if request.user.is_authenticated():
            template_name = 'ts/base.html'
            return render_to_response(template_name)
        else:
            return redirect('/testservice/login')

def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password1'])
            auth.login(request, newuser)
            return redirect('/testservice/')
        else:
            args['form'] = newuser_form
            return render_to_response('ts/register.html', args)
    else:
        return render_to_response('ts/register.html', args)    

def login(request):
    args={}
    args.update(csrf(request))
    args['form']=AuthenticationForm
    if request.POST:
        user_form = AuthenticationForm(data = request.POST)
        if user_form.is_valid():
            user = auth.authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            auth.login(request, user)
            return redirect('/testservice/')
        else:
            args['form'] = user_form
            return render_to_response('ts/login.html', args)
    else:
        return render_to_response('ts/login.html', args)    

def logout(request):
    auth.logout(request)
    return redirect('/testservice/')

def api_themes(request):
    if request.is_ajax():
        themes = Theme.objects.all()
        serialized_themes = serializers.serialize('json', themes)
        return HttpResponse(serialized_themes, 'json')
    return HttpResponse('Request must be set via AJAX')

@csrf_exempt
def api_tests(request):
    if request.is_ajax() & (request.method == "POST"):
        theme_pk = request.POST.get("theme_pk", "")
        tests = TestCase.objects.all()
        tests = tests.filter(theme_name__pk = theme_pk)
        serialized_tests = serializers.serialize('json', tests)
        return HttpResponse(serialized_tests, 'json')
    else:
        return HttpResponse('Request must be set via AJAX and POST')


def responseData(question, answers):
    response_data = {}
    response_data['question'] = question.name
    answer = []
    for ans in answers:
        answer.append([ans.pk, ans.name])
    response_data['answer'] = answer
    response_data['statistic'] = False
    return response_data
    
@csrf_exempt
@login_required
def api_dotest(request):
    if request.is_ajax() & (request.method == "POST"):
        test_pk = request.POST.get("test_pk","")
        testCase = TestCase.objects.all().get(pk = test_pk)
        
        # delete old statistic
        usertestCases = UserTestCaseAnswer.objects.filter(user = request.user)
        for usertestCase in usertestCases:
            testQuestions = TestQuestions.objects.filter(user_test_case_answer = usertestCase)
            for testQuestion in testQuestions:
                testQuestion.delete()
            usertestCase.delete()
            
        # create db for new statistic   
        userTestCaseAnswer = UserTestCaseAnswer(user = request.user, test_case_name = testCase)
        userTestCaseAnswer.save()
        
        questions = list(Question.objects.all().filter(test_name__pk = test_pk))
        question = questions.pop(0)
        answers = Answer.objects.all().filter(question__pk = question.pk)
               
        response_data = responseData(question, answers)

        return HttpResponse(json.dumps(response_data), content_type="application/json")        
    else:
        return HttpResponse('Request must be set via AJAX and POST')

@csrf_exempt
@login_required
def api_nextquestion(request):
    if request.is_ajax() & (request.method == "POST"):
        test_pk = request.POST.get("test_pk","")
        testCase = TestCase.objects.all().get(pk = test_pk)
        answer_pk = request.POST.get("answer_pk", "")
        userAnsw = Answer.objects.all().get(pk = answer_pk)
        question_pk = userAnsw.question.pk
        userTestCaseAnswer = UserTestCaseAnswer.objects.filter(user = request.user).get(test_case_name__pk = testCase.pk)
        userAnswer = UserAnswer(user_answer = userAnsw, user_test_case_answer = userTestCaseAnswer)
        userAnswer.save()
        question_pk += 1
        question = Question.objects.filter(test_name__pk = testCase.pk)
        question = list(question.filter(pk__gte = question_pk))
        if question:
            question = question.pop(0)
            answers = Answer.objects.filter(question__pk = question.pk)
            response_data = responseData(question, answers)
        else:
            userAnswers = UserAnswer.objects.all().filter(user_test_case_answer = userTestCaseAnswer)
            response_data = {}
            questions = []
            answerResult = []
            for userAnswer in userAnswers:
                question = Question.objects.get(pk = userAnswer.user_answer.question.pk)
                questions.append(question.name)
                answerResult.append([userAnswer.user_answer.isRight, userAnswer.user_answer.name])
            response_data['question'] = questions
            response_data['answerResult'] = answerResult
            userAnswersRight = userAnswers.filter(user_answer__isRight = True)
            response_data['countOfRightAnswers'] = len(userAnswersRight)
            response_data['statistic'] = True
            response_data['percent'] = (len(userAnswersRight) / len(userAnswers)) * 100
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse('Request must be set via AJAX and POST')
    
    

