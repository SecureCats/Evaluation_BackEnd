from django.urls import include, path
from . import views

urlpatterns = [
    path('api/', include([
        path('v1/', include([
            path('init', views.query_question_list)
        ]))
    ]))
]
