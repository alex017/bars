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


class IndexView(generic.TemplateView):
    template_name = 'ts/index.html'

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

