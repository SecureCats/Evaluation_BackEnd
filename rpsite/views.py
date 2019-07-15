from django.shortcuts import render, get_object_or_404, \
    get_list_or_404
from django.http import JsonResponse
from . import models
from .utils import test_pubkey
from django.conf import settings
import requests
import json

# Create your views here.


def query_question_list(request):
    classno = request.GET['classno']
    semester = request.GET['semester']
    course_list = get_list_or_404(
        models.Course,
        teaching_class__classno=classno,
        semester=semester
    )
    questions = []
    question_set = models.Question.objects.all()
    for question in question_set:
        question_obj = {
            'id': question.id,
            'description': question.question_text,
            'options': []
        }
        for option in question.option_set.all():
            question_obj['options'].append({
                'id': option.option_choice,
                'description': option.option_text
            })
        questions.append(question_obj)
    tasks = []
    for course in course_list:
        tasks.append({
            'id': course.course_no,
            'title': course.course_name,
            'status': 0,
            'questions': questions
        })
    return JsonResponse({
        'tasks': tasks
    })


def get_pubkey(classno, semester):
    if settings.PUBKEY_TESTING:
        return test_pubkey
    aip_site = settings.AIP_URL if settings.AIP_URL.endswith('/')  \
        else settings.AIP_URL + '/'
    res = requests.get('{}api/v1/pubkey/{}/{}'.format(aip_site,semester, classno))
    res_dic = json.loads(res.text)
    return {key:int(res_dic[key]) for key in res_dic}
