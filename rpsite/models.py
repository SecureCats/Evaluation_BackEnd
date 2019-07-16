from django.db import models

# Create your models here.
class Question(models.Model):

    class Meta:
        ordering = ['id']

    question_text = models.CharField('问题描述', max_length=100)

    def __str__(self):
        return self.question_text


class Option(models.Model):

    CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ]
    question = models.ForeignKey(Question, models.CASCADE)
    option_text = models.CharField("选项描述", max_length=100)
    option_choice = models.CharField('选项', max_length=1, choices=CHOICES)

    def __str__(self):
        return '{}-{}'.format(self.option_choice, self.option_text)

class TeachingClass(models.Model):
    # this class is just for many to many model relationship

    classno = models.CharField('班号', max_length=20)

    def __str__(self):
        return self.classno


class Course(models.Model):

    course_name = models.CharField('课程名称', max_length=20)
    course_no = models.CharField('课程编号', unique=True, max_length=20)
    semester = models.CharField('学期', max_length=20)
    teaching_class = models.ManyToManyField(TeachingClass)

    def __str__(self):
        return self.course_name


class Evaluation(models.Model):

    rnym = models.CharField("rnym", max_length=100)
    course = models.ForeignKey(Course, models.CASCADE)
    evaluated = models.BooleanField('是否已评', default=False)

    def __str__(self):
        return '{}-{}'.format(self.course.course_name, hex(int(self.rnym))[2:10])

class EvaluationItem(models.Model):

    option = models.ForeignKey(Option, models.CASCADE)
    evaluation = models.ForeignKey(Evaluation, models.CASCADE)

    def question(self):
        return self.option.question.question_text

    def __str__(self):
        return '{}-{}'.format(str(self.evaluation), self.option.question.id)
