from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^api/themes/$', views.api_themes, name = 'themes'),
    url(r'^api/tests/$', views.api_tests, name = 'tests'),
    url(r'^api/dotest/$', views.api_dotest, name = 'dotest'),
    url(r'^api/nextquestion/$', views.api_nextquestion, name = 'nextquestion'),
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    
]
