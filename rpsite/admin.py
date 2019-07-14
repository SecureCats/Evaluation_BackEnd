from django.contrib import admin
from . import models

# Register your models here.
class OptionInline(admin.StackedInline):
    model = models.Option
    extra = 2
    max_num = 4

@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

class StudentParticipation(admin.StackedInline):
    model = models.Course.teaching_class.through
    extra = 1

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [
        StudentParticipation
    ]
    exclude = ('teaching_class',)
    list_display = [
        '__str__', 'course_no', 'semeser'
    ]

@admin.register(models.TeachingClass)
class TeachingClass(admin.ModelAdmin):
    inlines = [
        StudentParticipation
    ]

class EvaluationItemInline(admin.StackedInline):
    model = models.EvaluationItem
    extra = 0
    fields = ['question', 'option']
    readonly_fields = ['question', 'option']

@admin.register(models.Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    inlines = [EvaluationItemInline]
