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
from .models import Theme, Question, Answer, TestCase
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
        theme = request.POST.get("theme", "")
        tests = TestCase.objects.all()
        tests = tests.filter(theme_name__name = theme)
        serialized_tests = serializers.serialize('json', tests)
        return HttpResponse(serialized_tests, 'json')
    else:
        return HttpResponse('Request must be set via AJAX and POST')

@csrf_exempt
def api_dotest(request):
    if request.is_ajax() & (request.method == "POST"):
        test_name = request.POST.get("test_name","")
        question_id = request.POST.get("question_id","")
        questions = Question.objects.all().filter(test_name__test_name = test_name)
        question = questions.get(id = question_id)
        answers = Answer.objects.all().filter(question__name = question.name)
        response_data = {}
        answer = []
        response_data['question'] = question.name
        for obj in answers:            
            answer.append(obj.name)
        response_data['answers'] = answer
        return HttpResponse(json.dumps(response_data), content_type="application/json")        
    else:
        return HttpResponse('Request must be set via AJAX and POST')
    
