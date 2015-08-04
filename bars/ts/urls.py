from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^register/$', views.register, name = 'register'),
    url(r'^login/$', views.login, name = 'login'),
    url(r'^logout/$', views.logout, name = 'logout'),
    url(r'^api/themes/$', views.api_themes, name = 'themes'),
    url(r'^$', views.IndexView.as_view(), name = 'index'),
    
]
