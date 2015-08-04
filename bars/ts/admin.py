from django.contrib import admin

from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from .models import Theme, Question, Answer, TestCase

class MyNestedStackedInline(NestedStackedInline):

    def queryset(self, request):
        return self.get_queryset(request)

class MyNestedStackedInline1(admin.TabularInline):
    
    def queryset(self, request):
        return self.get_queryset(request)
    
class AnswerAdmin(admin.TabularInline):
    model = Answer
    extra = 4
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question', {'fields' : ['name']}),
        ('Test case', {'fields' : ['test_name']}),
    ]
    inlines = [AnswerAdmin]
    list_display = ('name', 'test_name')
    list_filter = ['test_name']

class AnswerAdminInl(MyNestedStackedInline1):
    model = Answer
    extra = 4
    inlines=[]
    fk_name = 'question'
    
class QuestionListAdmin(MyNestedStackedInline):
    model = Question
    inlines = [AnswerAdminInl]
    extra = 4
    fk_name = 'test_name'
    
class TestCaseAdmin(NestedModelAdmin):
    model = TestCase
    fieldsets = [
        ('Test case name', {'fields' : ['test_name']}),
        ('Theme', {'fields': ['theme_name']}),
    ]
    inlines = [QuestionListAdmin]
    list_display = ('test_name', 'theme_name')
    list_filter = ['theme_name']
    
    
admin.site.register(Theme)
admin.site.register(Question, QuestionAdmin)
admin.site.register(TestCase, TestCaseAdmin)

