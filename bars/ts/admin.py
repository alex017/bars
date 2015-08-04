from django.contrib import admin

from .models import Theme, Question, Answer

admin.site.register(Theme)

admin.site.register(Question)

admin.site.register(Answer)
# Register your models here.
