from django.contrib import admin

from .models import Theme, Question, Answer

class AnswerAdmin(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields' : ['name']}),
     #   ('Theme', {'fields' : ['theme_name']}),
    ]
    inlines = [AnswerAdmin]
    #list_display = ('name', 'theme_name')
    #list_filter = ['theme_name']

admin.site.register(Theme)
admin.site.register(Question, QuestionAdmin)

