from django.urls import include, path
from . import views

urlpatterns = [
    path('api/', include([
        path('v1/', include([
            path('init/<str:classno>/<str:semaster>', views.query_question_list)
        ]))
    ]))
]
