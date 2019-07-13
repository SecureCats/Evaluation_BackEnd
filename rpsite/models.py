from django.db import models

# Create your models here.
class Question(models.Model):

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

