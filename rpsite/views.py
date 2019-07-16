from django.shortcuts import render, get_object_or_404, \
    get_list_or_404
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseForbidden
from . import models
from .utils import test_pubkey, verify
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

def verify_user(request):
    class_no = request.GET['classno']
    course_no = request.GET['course_no']
    course = get_object_or_404(models.Course, course_no=course_no)
    semester = course.semester
    required_param = (
        'Cs', 'Ce', 'Cv', 'Cw', 'C', 'Cx', 'Cz', 'x', 'rnym'
    )
    params = {}
    try:
        raw_json = json.loads(request.body)['credentials']
        for i in required_param:
            params[i] = int(raw_json[i])
        for i in range(1, 14):
            params['y{}'.format(i)] = int(raw_json['y{}'.format(i)])
        for i in range(1, 20):
            params['z{}'.format(i)] = int(raw_json['z{}'.format(i)])
    except:
        return HttpResponseBadRequest()
    pubkey = get_pubkey(class_no, semester)
    res = verify(pubkey, course_no, **params)
    if res:
        rnym = raw_json['rnym']
        eva = models.Evaluation.objects.filter(course__course_no=course_no, rnym=rnym)
        if eva:
            eva = eva[0]
            if eva.evaluated:
                return JsonResponse({'status': 'evaluated'})
            else:
                return JsonResponse({'status': 'accept'})
        else:
            eva = models.Evaluation(course=course, rnym=rnym)
            eva.save()
            return JsonResponse({'status': 'accept'})
    else:
        return JsonResponse({'status': 'denied'})

def submit_evaluation(request):
    try:
        classno = request.GET['classno']
        course_no = request.GET['course_no']
        raw_json = json.loads(request.body)
        rnym = raw_json['rnym']
        result = raw_json['result']
    except:
        return HttpResponseBadRequest()
    evaluation_set = models.Evaluation.objects.filter(course__course_no=course_no, rnym=rnym)
    if not evaluation_set:
        return HttpResponseForbidden()
    evaluation = evaluation_set[0]
    if evaluation.evaluated:
        return HttpResponseForbidden('already evaluated')
    question_set = models.Question.objects.all()
    for question in question_set:
        if question.id not in result:
            return HttpResponseBadRequest('not complete')
    for question in question_set:
        option = result[str(question.id)]
        question_option = get_object_or_404(models.Option, question=question, option_choice=option)
        evaluation_item = models.EvaluationItem(option=question_option, evaluation=evaluation)
        evaluation_item.save()

