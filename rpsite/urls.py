from django.urls import include, path
from . import views

urlpatterns = [
    path('api/', include([
        path('v1/', include([
            path('init', views.query_question_list),
            path('auth', views.verify_user),
            path('result', views.submit_evaluation),
        ]))
    ]))
]
